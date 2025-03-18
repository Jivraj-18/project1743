from flask import request, jsonify
from flask_restful import Api, Resource, reqparse, fields, marshal, marshal_with
from flask_security import current_user, logout_user, auth_required, roles_required, roles_accepted
from sqlalchemy import text, func
from .models import Instructor, Student, Course, User, user_roles, Issue, CourseStudent, Content, Question, AssignmentStudent, Assignment, Event, UserTask, StarredQuestion
from .extensions import db
from datetime import datetime, timezone
import base64
import json
from .evaluate import evaluate_assignment, evaluate_programming


from .sb import makeS
from .ai import ink

api=Api(prefix='/api')

# for login
class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        
        user = db.session.query(User).filter_by(email=email).first()
        student = db.session.query(Student).filter_by(email=email).first()
        instructor = db.session.query(Instructor).filter_by(email=email).first()
        
        if user and user.active:
            roles = [role.name for role in user.roles]
            if student:
                return {
                    "token": user.get_auth_token(),
                    "roles": roles,
                    "id": user.user_id,
                    "student_id": student.student_id
                }, 200
            elif instructor:
                return {
                    "token": user.get_auth_token(),
                    "roles": roles,
                    "id": user.user_id,
                    "instructor_id": instructor.instructor_id
                }, 200
        
        return {"message": 'Invalid credentials'}, 401

# for logout        
class Logout(Resource):
    def get(self):
        logout_user() 
        return {'message': 'Logged out successfully'}, 200
    
# for student info
class StudInfo(Resource):
    @roles_required('student')
    def get(self):
        user_id = current_user.user_id
        
        user = db.session.get(User, user_id)
        if not user:
            return {'message': 'User not found'}, 404

        student = db.session.query(Student).filter_by(email=user.email).first()
        if not student:
            return {'message': 'Student record not found'}, 404
        output={
                'student_name': student.student_name,
                'enroll_date': student.enroll_date,
                'current_level': student.current_level,
                'dob': student.dob,
                'about_me' : student.about_me,
                'phone' : student.phone,
                'address': student.address,
                'email' : student.email,
            }
        return jsonify(output)

# to report issues   
class Report(Resource):
    @roles_required('student')
    def post(self):
        data = request.get_json()
        issue_type = data.get('issue_type')
        user_id = data.get('user_id')
        course_id = data.get('course_id')  
        subject = data.get('subject')  
        description = data.get('description')

        report = Issue(issue_type=issue_type, user_id=user_id, subject=subject, description=description, course_id=course_id, issue_date=datetime.now(timezone.utc))

        db.session.add(report)
        db.session.commit()

        return {'message': 'Issue reported successfully', 'issue_id': report.issue_id}, 200

    @roles_required('student')    
    def get(self, user_id):
        issues = db.session.query(Issue).join(Course, Issue.course_id == Course.course_id, isouter=True).filter(Issue.user_id == user_id).all()
        result = [{'issue_id': issue.issue_id, 'issue_type': issue.issue_type, 'course_name': issue.course.course_name if issue.course else None, 'subject': issue.subject, 'description': issue.description, 'issue_date': issue.issue_date, 'solution': issue.solution, 'resolved': issue.resolved} for issue in issues]
        return jsonify(result)

# to view reports
class ViewReports(Resource):
    @roles_accepted('instructor', 'ta')    
    def get(self):
        issues = db.session.query(Issue).join(User, Issue.user_id == User.user_id).join(Course, Issue.course_id == Course.course_id, isouter=True).filter(Issue.resolved == False).all()
        result = [{'issue_id': issue.issue_id, 'issue_type': issue.issue_type, 'course_name': issue.course.course_name if issue.course else None, 'user_email': issue.user.email, 'subject': issue.subject, 'description': issue.description, 'issue_date': issue.issue_date} for issue in issues]
        return jsonify(result)

# to get events
class Events(Resource):
    def get(self):
        events = db.session.query(Event).all()
        result = [{'event_id': event.event_id, 'title': event.title, 'date': event.date, 'description': event.description} for event in events]
        return jsonify(result)
    
# to get and add tasks
class Tasks(Resource):
    @auth_required('token')
    def get(self):
        user_id = current_user.user_id  
        
        tasks = db.session.query(UserTask).filter_by(user_id=user_id).all()
        result = [{'task_id': task.task_id, 'title': task.title, 'description': task.description, 'task_date': task.task_date} for task in tasks]
        
        return jsonify(result)
    
    @auth_required('token')
    def post(self):
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        task_date_str = data.get('task_date')

        # Ensure required fields are provided
        if not title or not task_date_str:
            return {"error": "Missing required fields"}, 400

        try:
            task_date = datetime.strptime(task_date_str, "%Y-%m-%d").date()
        except ValueError:
            return {"error": "Invalid date format, expected YYYY-MM-DD"}, 400

        # Assign task to the logged-in user
        user_id = current_user.user_id  
        task = UserTask(title=title, description=description, task_date=task_date, user_id=user_id)

        db.session.add(task)
        db.session.commit()

        return {'message': 'Task created successfully', 'task_id': task.task_id}, 201

    @auth_required('token')
    def delete(self, task_id):
        if not current_user.is_authenticated:
            return {"error": "You must sign in to view this resource."}, 401

        task = db.session.get(UserTask, task_id)
        
        if not task:
            return {'message': 'Task not found'}, 404

        # Ensure only the owner of the task can delete it
        if task.user_id != current_user.user_id:
            return {'error': 'Unauthorized to delete this task'}, 403

        db.session.delete(task)
        db.session.commit()

        return {'message': 'Task deleted successfully'}, 200
    
# to get courses for a student
class MyCourses(Resource):
    def get(self, student_id):
        student = db.session.get(Student, student_id)
        if not student:
            return {'message': 'Student not found'}, 404

        courses = (
            db.session.query(Course.course_name, Assignment.assignment_id, Assignment.total_marks, AssignmentStudent.marks_obtained)
            .join(CourseStudent, Course.course_id == CourseStudent.course_id)
            .join(Assignment, Course.course_id == Assignment.course_id)
            .join(AssignmentStudent, Assignment.assignment_id == AssignmentStudent.assignment_id)
            .filter(CourseStudent.student_id == student_id)
            .all()
        )

        course_data = {}
        for course_name, assignment_id, total_marks, marks_obtained in courses:
            if course_name not in course_data:
                course_data[course_name] = []
            
            percentage = (int(marks_obtained) / total_marks) * 100 if total_marks else 0
            course_data[course_name].append({
                "assignment_id": assignment_id,
                "percentage": round(percentage, 2)
            })

        return jsonify(course_data)

# to get course content     
class CourseContent(Resource):
    def get(self, course_id):
        course = db.session.get(Course, course_id)
        if not course:
            return {'message': 'Course not found'}, 404

        contents = db.session.query(Content).filter_by(course_id=course_id).all()

        response = {
            "course_id": course.course_id,
            "course_name": course.course_name,
            "description": course.description,
            "contents": [
                {
                    "content_id": content.content_id,
                    "content_type": content.content_type,
                    "content_name": content.content_name,
                    "url": content.url,
                    "transcript_url": content.transcript_url
                }
                for content in contents
            ]
        }

        if not contents:
            response["message"] = "No content found for this course"

        return jsonify(response)
    
    @roles_accepted('instructor','ta')
    def post(self):
        data = request.get_json()
        content = Content(
            course_id=data.get('course_id'),
            content_type=data.get('content_type'),
            content_name=data.get('content_name'),
            url=data.get('url'),
            transcript_url=data.get('transcript_url')
        )
        db.session.add(content)
        db.session.commit()
        return {'message': 'Content created successfully', 'content_id': content.content_id}, 201

    @roles_accepted('instructor','ta')
    def put(self, content_id):
        data = request.get_json()
        content = db.session.query(Content).get(content_id)
        if not content:
            return {'error': 'Content not found'}, 404

        content.course_id = data.get('course_id', content.course_id)
        content.content_type = data.get('content_type', content.content_type)
        content.content_name = data.get('content_name', content.content_name)
        content.url = data.get('url', content.url)
        content.transcript_url = data.get('transcript_url', content.transcript_url)

        db.session.commit()
        return {'message': 'Content updated successfully'}

    
# to add or edit questions
class Questions(Resource):

    @roles_required('instructor')
    def post(self):
        data = request.get_json()

        if not data or not isinstance(data, dict):  # Ensure input is a dictionary
            return jsonify({"error": "Invalid input format. Expected a dictionary."}), 400

        # Extract assignment details
        category = data.get("category")
        course_id = data.get("course_id")
        which_week = data.get("which_week")
        total_marks = sum(q.get("marks", 0) for q in data.get("questions", []))

        if not category or not course_id or which_week is None:
            return jsonify({"error": "Missing required assignment details"}), 400

        # Create the assignment
        new_assignment = Assignment(
            category=category,
            course_id=course_id,
            which_week=which_week,
            total_marks=total_marks
        )
        db.session.add(new_assignment)
        db.session.commit()  # Commit to get assignment_id

        added_questions = []

        for q in data.get("questions", []):
            correct_options = q.get("correct_options")

            # Convert correct_options to JSON string if it's a list (for programming Qs)
            if isinstance(correct_options, list):
                correct_options = json.dumps(correct_options)

            question = Question(
                question_type=q.get("question_type"),
                assignment_id=new_assignment.assignment_id,
                question=q.get("question"),
                options=base64.b64encode(json.dumps(q.get("options")).encode()).decode() if q.get("options") else None,
                correct_options=correct_options,
                marks=q.get("marks"),
                hints=q.get("hints"),
                text_solution=q.get("text_solution")
            )
            db.session.add(question)
            db.session.commit()

            # Decode correct_options only if it is JSON (list)
            try:
                parsed_correct_options = json.loads(correct_options)
            except (json.JSONDecodeError, TypeError):
                parsed_correct_options = correct_options

            added_questions.append({
                "question_id": question.question_id,
                "assignment_id": question.assignment_id,
                "question_type": question.question_type,
                "question": question.question,
                "options": q.get("options"),
                "correct_options": parsed_correct_options,
                "marks": question.marks,
                "hints": question.hints,
                "text_solution": question.text_solution
            })

        return {
            "message": "Assignment and questions added successfully"
        }, 201
        
    def put(self, question_id):
        data = request.get_json()
        question = db.session.query(Question).get(question_id)            

        if not question:
            return {'message': 'Question not found'}, 404

        question.question_type = data.get('question_type', question.question_type)
        question.assignment_id = data.get('assignment_id', question.assignment_id)
        question.question = data.get('question', question.question)

        options = data.get('options')
        if options:
            question.options = base64.b64encode(json.dumps(options).encode()).decode()

        question.correct_options = data.get('correct_options', question.correct_options)
        question.marks = data.get('marks', question.marks)
        question.hints = data.get('hints', question.hints)
        question.text_solution = data.get('text_solution', question.text_solution)

        db.session.commit()
        return {'message': 'Question updated successfully'}, 200

# to show starred questions to student
class StarredQuestions(Resource):
    def get(self, student_id):
        starred_questions = (
            db.session.query(Question)
            .join(StarredQuestion, Question.question_id == StarredQuestion.question_id)
            .join(Assignment, Question.assignment_id == Assignment.assignment_id)
            .filter(StarredQuestion.student_id == student_id)
            .all()
        )

        if not starred_questions:
            return {'message': 'No starred questions found'}, 404

        result = [
            {
                'question_id': q.question_id,
                'question_type': q.question_type,
                'assignment_id': q.assignment_id,
                'assignment_category': q.assignment.category,
                'which_week': q.assignment.which_week,
                'question': q.question,
                'options': json.loads(base64.b64decode(q.options).decode()) if q.options else None,
                'correct_options': q.correct_options,
                'marks': q.marks,
                'hints': q.hints,
                'text_solution': q.text_solution
            }
            for q in starred_questions
        ]

        return jsonify(result)
    
# to get students scores info
class AssignmentSubmissions(Resource):
    @roles_required('instructor')
    def get(self):
        assignments = (
            db.session.query(
                Assignment.course_id, 
                Assignment.assignment_id, 
                Assignment.which_week, 
                Assignment.category,
                AssignmentStudent
            )
            .join(Assignment, AssignmentStudent.assignment_id == Assignment.assignment_id)
            .order_by(Assignment.course_id)
            .all()
        )

        course_wise_data = {}

        for course_id, assignment_id, which_week, category, submission in assignments:
            if course_id not in course_wise_data:
                course_wise_data[course_id] = {"course_id": course_id, "assignments": []}

            marks_answers = None
            if submission.marks_answers and submission.marks_answers.strip():
                try:
                    marks_answers = json.loads(submission.marks_answers)
                except json.JSONDecodeError:
                    marks_answers = None  # Handle invalid JSON gracefully

            course_wise_data[course_id]["assignments"].append({
                "assignment_id": assignment_id,
                "which_week": which_week,
                "category": category,
                "id": submission.id,
                "student_id": submission.student_id,
                "marks_answers": marks_answers,
                "marks_obtained": submission.marks_obtained,
                "code": submission.code,
                "submission_date": submission.submission_date.strftime("%Y-%m-%dT%H:%M:%S")
            })

        return jsonify(list(course_wise_data.values()))


# to get questions for an assignment and submit answers    
class Assignments(Resource):
    def post(self):
        data = request.get_json()

        student_id = data.get("student_id")
        assignment_id = data.get("assignment_id")
        student_answers = data.get("student_answers")
        code = data.get("code")

        if not student_id or not assignment_id:
            return jsonify({"error": "Missing required fields"}), 400
        
        if student_answers=={}:
            return {'error':'No answers provided'}, 400

        if isinstance(student_answers, list):
            student_answers = {str(i): ans for i, ans in enumerate(student_answers)}

        existing_entry = (
            db.session.query(AssignmentStudent)
            .filter(AssignmentStudent.student_id == student_id, AssignmentStudent.assignment_id == assignment_id)
            .first()
        )
        if existing_entry:
            db.session.delete(existing_entry)
            db.session.commit()


        if code:
            if not student_answers or len(student_answers) != 1:
                return {"error": "Programming questions require exactly one question_id"}, 400
            result, total_marks = evaluate_programming(assignment_id, student_answers)
        else:
            result, total_marks = evaluate_assignment(assignment_id, student_answers)

        encoded_result = base64.b64encode(json.dumps(result).encode()).decode()

        new_submission = AssignmentStudent(
            student_id=student_id,
            assignment_id=assignment_id,
            marks_obtained=total_marks,
            marks_answers=encoded_result,
            code=code if code else None,
            submission_date=datetime.now(timezone.utc)
        )

        db.session.add(new_submission)
        db.session.commit()

        return {
            "message": "Assignment submitted successfully",
            "total_marks": total_marks,
            "details": result
        }, 201
    
    def get(self, assignment_id, student_id):
        assignment_submission = (
            db.session.query(AssignmentStudent)
            .filter(AssignmentStudent.assignment_id == assignment_id, AssignmentStudent.student_id == student_id)
            .first()
        )

        questions = (
            db.session.query(Question)
            .filter(Question.assignment_id == assignment_id)
            .all()
        )

        question_list = []
        for q in questions:
            try:
                options = json.loads(base64.b64decode(q.options).decode()) if q.options else None
            except (json.JSONDecodeError, TypeError):
                options = None  # Handle decoding errors

            question_list.append({
                'question_id': q.question_id,   
                'question_type': q.question_type,
                'question': q.question,
                'options': options,
                'correct_options': q.correct_options,
                'marks': q.marks,
                'hints': q.hints,
                'text_solution': q.text_solution
            })

        submission_data = None
        if assignment_submission:
            submission_data = {
                'marks_answers': json.loads(base64.b64decode(assignment_submission.marks_answers).decode()) if assignment_submission.marks_answers else None,
                'marks_obtained': assignment_submission.marks_obtained,
                'code': assignment_submission.code or "",  # Ensure None values are handled
                'submission_date': assignment_submission.submission_date.strftime("%Y-%m-%dT%H:%M:%S") if assignment_submission.submission_date else None
            }

        response = {
            'questions': question_list,
            'submission': submission_data  # Will be `None` if no submission exists
        }

        return jsonify(response)  # No ", 200"

class Editdeadline(Resource):
    def put(self, assignment_id):
        data = request.get_json()

        # Find the assignment by ID
        assignment = db.session.query(Assignment).filter_by(assignment_id=assignment_id).first()

        if not assignment:
            return {"error": "Assignment not found"}, 404 

        if "deadline" in data:
            try:
                assignment.deadline = datetime.strptime(data["deadline"], "%Y-%m-%dT%H:%M:%S") if data["deadline"] else None
            except ValueError:
                return {"error": "Invalid datetime format"}, 400

        # Save updates
        db.session.commit()

        return {"message": "Assignment updated successfully"}, 200



# to
class AI(Resource):

    def post(self):

        try :
            s = request.get_json() if request.is_json else {}

            t = s.get("type", "")
            p = s.get("prompt", "")
            b = s.get("background", {})

            if not isinstance(t, str) or not isinstance(p, str) or not isinstance(b, dict):
                b = {"res": "Oops, BAD Request", "error" : True}, 400
                return b

            link = {
                "gen" : ink.generate_questions,
                "sumup" : ink.summarize,
                "chat" : ink.chat,
                "analyse" : ink.chat,
                "explain" : ink.chat
            }

            if t in link:
                c = makeS(b, t)
                i = { 
                    "prompt" : p,
                    "content" : c
                }
                # print("API => ", c, i)
                d = link[t](i)
            else :
                b = {"res": "Oops, Invalid Type", "error" : True}, 400
                return b

            b = jsonify({"res" : json.dumps(d)})
            return b
        except Exception as e:
            print("Error : ", e)
            b = { "res" : "Internal Server Error", "error" : True }, 500
            return b

api.add_resource(AI, '/ai')


api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(StudInfo, '/studinfo/<int:student_id>')
api.add_resource(Report, '/report', '/report/<int:user_id>')
api.add_resource(ViewReports, '/view_reports')
api.add_resource(Events, '/events')
api.add_resource(Tasks, '/tasks/<int:user_id>', '/tasks', '/tasks/delete/<int:task_id>')
api.add_resource(MyCourses, '/mycourses/<int:student_id>')
api.add_resource(CourseContent, '/content/<int:course_id>', '/content', '/content/edit/<int:content_id>')
api.add_resource(Questions, '/questions', '/questions/<int:question_id>')
api.add_resource(StarredQuestions, '/starred_questions/<int:student_id>')
api.add_resource(AssignmentSubmissions, '/submissions')
api.add_resource(Assignments, '/assignments/<int:assignment_id>/<int:student_id>', '/assignments')
api.add_resource(Editdeadline, '/edit_assignment/<int:assignment_id>')






