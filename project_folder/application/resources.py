from flask import request, jsonify
from flask_restful import Api, Resource, reqparse, fields, marshal, marshal_with
from flask_security import current_user, logout_user, auth_required, roles_required
from sqlalchemy import text, func
from .models import Instructor, Student, Course, User, user_roles, Feedback, CourseStudent, Content, Question, AssignmentStudent, Assignment
from .extensions import db
from datetime import datetime
import base64
import json

api=Api(prefix='/api')

# for login
class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        user = db.session.query(User).filter_by(email=email).first()
        if user and user.active:
            return {"token": user.get_auth_token(), "role": user.roles[0].name, "id": user.user_id}, 200
        else:
            return {"message": 'Invalid credentials'}, 401    

# for logout        
class Logout(Resource):
    def get(self):
        logout_user() 
        return {'message': 'Logged out successfully'}, 200

# for reporting issues    
class Report(Resource):
    def post(self):
        data = request.get_json()
        student_id = data.get('student_id')  
        rating = data.get('rating', 0)  
        review = data.get('review')
        content_id = data.get('content_id', None)  

        report = Feedback(type="issue report", rating=rating, review=review, content_id=content_id, student_id=student_id)

        db.session.add(report)
        db.session.commit()

        return {'message': 'Issue reported successfully', 'feedback_id': report.feedback_id}, 201

# to get courses for a student
class MyCourses(Resource):
    def get(self, student_id):
        student = db.session.get(Student, student_id)
        if not student:
            return {'message': 'Student not found'}, 404

        courses = db.session.query(Course).join(CourseStudent).filter(CourseStudent.student_id == student_id).all()

        if not courses:
            return {'message': 'No courses found for this student'}, 404

        result = [{'course_id': course.course_id, 'course_name': course.name} for course in courses]
        return jsonify(result)

# to get course content     
class CourseContent(Resource):
    def get(self, course_id):
        course = db.session.get(Course, course_id)
        if not course:
            return {'message': 'Course not found'}, 404

        contents = db.session.query(Content).filter_by(course_id=course_id).all()

        if not contents:
            return {'message': 'No content found for this course'}, 404

        result = [
            {
                'content_id': content.content_id,
                'content_type': content.content_type,
                'url': content.url,
                'transcript_url': content.transcript_url
            }
            for content in contents
        ]
        return jsonify(result)

# to get questions for an assignment and submit answers    
class Assignments(Resource):
    def post(self):
        data = request.get_json()
        assignment_id = data.get('assignment_id')
        student_id = data.get('student_id')
        answers = data.get('answers') 
            
        if not assignment_id or not student_id or not answers:
            return {'error': 'Missing required fields'}, 400
            
        marks_answers = {}
        total_marks = 0
            
        for question_id, student_answer in answers.items():
            question = db.session.query(Question).get(question_id)            
            if question:
                awarded_marks = question.marks if student_answer == question.correct_options else 0
                total_marks += awarded_marks
                marks_answers[question_id] = {'student_answer': student_answer, 'marks': awarded_marks}
                
        marks_answers['total_marks'] = total_marks
        marks_answers_base64 = base64.b64encode(json.dumps(marks_answers).encode()).decode()
            
        assignment_student = AssignmentStudent(
            assignment_id=assignment_id,
            student_id=student_id,
            marks_answers=marks_answers_base64
        )
            
        db.session.add(assignment_student)
        db.session.commit()
        return {'message': 'Answers submitted successfully', 'total_marks': total_marks}, 201
        
    def get(self, assignment_id):
        questions = db.session.query(Question).filter_by(assignment_id=assignment_id).all()

        if not questions:
            return {'message': 'No questions found for this assignment'}, 404
        
        result = []
        for question in questions:
            options = json.loads(base64.b64decode(question.options).decode()) if question.options else None
            result.append({
                'question_id': question.question_id,
                'type': question.type,
                'assignment_id': question.assignment_id,
                'question': question.question,
                'options': options,
                'correct_options': question.correct_options,
                'marks': question.marks,
                'hints': question.hints,
                'text_solution': question.text_solution
            })
        
        return result, 200

# to add or edit questions
class Questions(Resource):
    def post(self):
        data = request.get_json()
        options = data.get('options')
        
        if options:
            options_base64 = base64.b64encode(json.dumps(options).encode()).decode()
        else:
            options_base64 = None
        
        question = Question(
            type=data.get('type'),
            assignment_id=data.get('assignment_id'),
            question=data.get('question'),
            options=options_base64,
            correct_options=data.get('correct_options'),
            marks=data.get('marks'),
            hints=data.get('hints'),
            text_solution=data.get('text_solution')
        )
        db.session.add(question)
        db.session.commit()
        return {'message': 'Question added successfully'}, 201

    def put(self, question_id):
        data = request.get_json()
        question = db.session.query(Question).get(question_id)            


        if not question:
            return {'message': 'Question not found'}, 404

        question.type = data.get('type', question.type)
        question.assignment_id = data.get('assignment_id', question.assignment_id)
        question.question = data.get('question', question.question)

        options = data.get('options')
        if options:
            question.options = base64.b64encode(json.dumps(options).encode()).decode()
        elif options is None:
            question.options = None

        question.correct_options = data.get('correct_options', question.correct_options)
        question.marks = data.get('marks', question.marks)
        question.hints = data.get('hints', question.hints)
        question.text_solution = data.get('text_solution', question.text_solution)

        db.session.commit()
        return {'message': 'Question updated successfully'}, 200

# to get student marks for a course
class CourseResults(Resource):
    def get(self, course_id):
        results = (
            db.session.query(AssignmentStudent, Assignment)
            .join(Assignment, Assignment.assignment_id == AssignmentStudent.assignment_id)
            .filter(Assignment.course_id == course_id)
            .all()
        )

        output = []
        for assignment_student, assignment in results:
            decoded_marks_answers = base64.b64decode(assignment_student.marks_answers).decode()
            marks_answers_json = json.loads(decoded_marks_answers)

            output.append({
                'assignment_id': assignment.assignment_id,
                'category': assignment.category,
                'student_id': assignment_student.student_id,
                'marks_answers': marks_answers_json
            })

        return jsonify(output)

# to get students in a particular course
class CourseStudents(Resource):
    def get(self, course_id):
        students = (
            db.session.query(Student)
            .join(CourseStudent, CourseStudent.student_id == Student.student_id)
            .filter(CourseStudent.course_id == course_id)
            .all()
        )

        output = [
            {
                'student_id': student.student_id,
                'student_name': student.student_name,
                'email': student.email,
                'phone': student.phone,
                'current_level': student.current_level
            }
            for student in students
        ]

        return jsonify(output)

# to add and edit content of a course
class EditContent(Resource):
    def post(self):
        data = request.get_json()
        content = Content(
            course_id=data.get('course_id'),
            content_type=data.get('content_type'),
            url=data.get('url'),
            transcript_url=data.get('transcript_url')
        )
        db.session.add(content)
        db.session.commit()
        return {'message': 'Content created successfully', 'content_id': content.content_id}, 201

    def put(self, content_id):
        data = request.get_json()
        content = db.session.query(Content).get(content_id)
        if not content:
            return {'error': 'Content not found'}, 404

        content.course_id = data.get('course_id', content.course_id)
        content.content_type = data.get('content_type', content.content_type)
        content.url = data.get('url', content.url)
        content.transcript_url = data.get('transcript_url', content.transcript_url)

        db.session.commit()
        return {'message': 'Content updated successfully'}


class random(Resource):
    def get(self):
        return {  "ramdom" : "Hello There!!" }



api.add_resource(random, '/random')

api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Report, '/report')
api.add_resource(MyCourses, '/mycourses/<int:student_id>/')
api.add_resource(CourseContent, '/course/<int:course_id>/content')
api.add_resource(Questions, '/question', '/question/<int:question_id>')
api.add_resource(CourseResults, '/results/<int:course_id>')
api.add_resource(CourseStudents, '/students/<int:course_id>')
api.add_resource(Assignments, '/assignment/answers', '/assignment/<int:assignment_id>')
api.add_resource(EditContent, '/content', '/content/<int:content_id>')
