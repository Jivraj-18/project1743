from .models import Question
from .extensions import db
import base64
import json
import re

# Function to fetch questions for a given assignment_id
def get_questions_for_assignment(assignment_id):
    questions_table = db.session.query(Question).filter_by(assignment_id=assignment_id).all()

    formatted_questions = [
        {
            "question_id": str(q.question_id),
            "assignment_id": q.assignment_id,
            "question_type": q.question_type,
            "question": q.question,
            "options": json.loads(base64.b64decode(q.options).decode()) if q.options else None,
            "correct_options": q.correct_options,
            "marks": q.marks,
            "hints": q.hints,
            "text_solution": q.text_solution
        }
        for q in questions_table
    ]

    return formatted_questions


# Function to evaluate assignment (MCQ, MSQ, NAT)
def evaluate_assignment(assignment_id, student_answers):
    questions_table = get_questions_for_assignment(assignment_id)
    
    result = {}
    total_marks = 0
    question_dict = {str(q["question_id"]): q for q in questions_table}

    for q_id, student_answer in student_answers.items():
        question = question_dict[q_id]
        correct_answer = question["correct_options"]
        marks = question["marks"]
        question_type = question["question_type"]

        if question_type == "MCQ":
            obtained_marks = marks if student_answer == correct_answer else 0

        elif question_type == "MSQ":
            correct_set = set(correct_answer.split(","))
            student_set = set(student_answer.split(","))

            if not student_set.issubset(correct_set):
                obtained_marks = 0
            else:
                per_option_mark = marks / len(correct_set)
                obtained_marks = round((per_option_mark * len(student_set)), 2)

        elif question_type == "NAT":
            obtained_marks = marks if student_answer == correct_answer else 0

        result[q_id] = {"marked_answers": student_answer, "marks": obtained_marks}
        total_marks += obtained_marks

    return result, total_marks


# Extract function name from code string
def extract_function_name(text):
    match = re.search(r'function\s+(\w+)', text)
    return match.group(1) if match else None


# Function to evaluate programming questions
def evaluate_programming(assignment_id, student_answer):
    questions_table = get_questions_for_assignment(assignment_id)

    result = {}
    total_marks = 0
    cases_passed = 0

    question_dict = {str(q["question_id"]): q for q in questions_table}
    q_id = list(student_answer.keys())[0]
    question = question_dict[q_id]
    ques_text = question["question"]
    func_name = extract_function_name(ques_text) 
    pvt_cases = question["correct_options"]
    marks = question["marks"]
    namespace = {}
    code = list(student_answer.values())[0]

    exec(code, namespace) 
    func = namespace[func_name]

    for cases in pvt_cases:
        inp = cases["input"]
        exp_out = cases["expected_output"]
        if isinstance(inp, (list, tuple)):
            output = func(*inp)  
        else:
            output = func(inp) 
        if str(output) == exp_out:
            total_marks += round((marks / len(pvt_cases)), 2)
            cases_passed += 1

    return {q_id: {"cases_passed": cases_passed, "marks": round(total_marks, 2)}}, round(total_marks, 2)

