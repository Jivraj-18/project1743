from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean, Table
from sqlalchemy.orm import relationship, declarative_base
from flask_security import UserMixin, RoleMixin

Base = declarative_base()

user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('User.user_id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('Role.role_id'), primary_key=True),
)

class User(Base, UserMixin):
    __tablename__ = 'User'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    fs_uniquifier = Column(String, nullable=False, unique=True)
    email = Column(ForeignKey('Student.email'), ForeignKey('Instructor.email'), nullable=False, unique=True)
    active = Column(Boolean, default=True)

    Student = relationship('Student', uselist=False, back_populates='user', overlaps="Instructor")
    Instructor = relationship('Instructor', uselist=False, back_populates='user', overlaps="Student")
    roles = relationship('Role', secondary=user_roles)

class Role(Base, RoleMixin):
    __tablename__ = 'Role'
    role_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)

class Instructor(Base):
    __tablename__ = 'Instructor'
    instructor_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)

    user = relationship('User', uselist=False, back_populates='Instructor', overlaps="Student")

class Student(Base):
    __tablename__ = 'Student'
    student_id = Column(Integer, primary_key=True, autoincrement=True)
    student_name = Column(String, nullable=False)
    enroll_date = Column(DateTime)
    current_level = Column(String, default="foundation")
    dob = Column(DateTime)
    about_me = Column(String)
    phone = Column(Integer, unique=True)
    email = Column(String, nullable=False, unique=True)

    user = relationship('User', uselist=False, back_populates='Student', overlaps="Instructor,user")

class Course(Base):
    __tablename__ = 'Course'
    course_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)

class CourseStudent(Base):
    __tablename__ = 'Course_student'
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(ForeignKey('Student.student_id'))
    course_id = Column(ForeignKey('Course.course_id'))

    course = relationship('Course')
    student = relationship('Student')

class InstructorCourse(Base):
    __tablename__ = 'Instructor_course'
    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(ForeignKey('Course.course_id'))
    instructor_id = Column(ForeignKey('Instructor.instructor_id'))

    course = relationship('Course')
    instructor = relationship('Instructor')

class Content(Base):
    __tablename__ = 'Content'
    content_id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(ForeignKey('Course.course_id'), nullable=False)
    content_type = Column(String, nullable=False)
    url = Column(String, unique=True)
    transcript_url = Column(String, unique=True)
    ai_summary = Column(String)

    course = relationship('Course')

class Assignment(Base):
    __tablename__ = 'Assignment'
    assignment_id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String, nullable=False)
    course_id = Column(ForeignKey('Course.course_id'), nullable=False)
    deadline = Column(DateTime, nullable=False)
    which_week = Column(DateTime, nullable=False)

    course = relationship('Course')

class Question(Base):
    __tablename__ = 'Question'
    question_id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)
    assignment_id = Column(ForeignKey('Assignment.assignment_id'), nullable=False)
    question = Column(String, nullable=False)
    options = Column(String)
    correct_options = Column(String, nullable=False)
    marks = Column(Integer, nullable=False)
    hints = Column(String)
    text_solution = Column(String)

    assignment = relationship('Assignment')

class AssignmentStudent(Base):
    __tablename__ = 'Assignment_student'
    id = Column(Integer, primary_key=True, autoincrement=True)
    assignment_id = Column(ForeignKey('Assignment.assignment_id'))
    student_id = Column(ForeignKey('Student.student_id'))
    marks_answers = Column(String, nullable=False)
    submission_date = Column(DateTime, nullable=False)

    assignment = relationship('Assignment')
    student = relationship('Student')

class Feedback(Base):
    __tablename__ = 'Feedback'
    feedback_id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)
    student_id = Column(ForeignKey('Student.student_id'), nullable=False)
    subject = Column(String, nullable=False)
    description = Column(String, nullable=False)
 
    student = relationship('Student')

class ActionLog(Base):
    __tablename__ = 'Action_log'
    action_id = Column(Integer, primary_key=True, autoincrement=True)
    action = Column(String) 
    date = Column(DateTime, nullable=False) 
    type = Column(String)  
    user_id = Column(ForeignKey('User.user_id'), nullable=False) 

    user = relationship('User') 

class Event(Base):
    __tablename__ = 'News'
    news_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey('User.user_id'), nullable=False) 
    title = Column(String) 
    date = Column(DateTime, nullable=False) 
    description = Column(String)
    deadline = Column(DateTime, nullable=False)

    user = relationship('User') 

class UserTask(Base):
    __tablename__ = 'User_task'
    task_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey('User.user_id'), nullable=False) 
    title = Column(String) 
    description = Column(String)
    task_date = Column(DateTime, nullable=False)

    user = relationship('User') 

class StarredQuestion(Base):
    __tablename__ = 'Starred_question'
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(ForeignKey('Student.student_id'), nullable=False)
    question_id = Column(ForeignKey('Question.question_id'), nullable=False)
    starred = Column(Boolean, default=True)

    student = relationship('Student')
    question = relationship('Question')

