# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app import db
Base = declarative_base()
metadata = Base.metadata


class Course(Base):
    __tablename__ = 'Course'

    course_id = Column(Integer, primary_key=True, server_default=text("nextval('\"Course_course_id_seq\"'::regclass)"))
    name = Column(String, nullable=False)
    description = Column(String)


class Instructor(Base):
    __tablename__ = 'Instructor'

    instructor_id = Column(Integer, primary_key=True, server_default=text("nextval('\"Instructor_instructor_id_seq\"'::regclass)"))
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)


class Role(Base):
    __tablename__ = 'Role'

    role_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)


class Student(Base):
    __tablename__ = 'Student'

    student_id = Column(Integer, primary_key=True, server_default=text("nextval('\"Student_student_id_seq\"'::regclass)"))
    Student_name = Column(Integer, nullable=False)
    enroll_date = Column(DateTime)
    current_level = Column(String, server_default=text("'foundation'::character varying"))
    dob = Column(DateTime)
    about_me = Column(String)
    phone = Column(Integer, unique=True)
    email = Column(String, nullable=False, unique=True)


class Assignment(Base):
    __tablename__ = 'Assignment'

    assignment_id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False)
    course_id = Column(ForeignKey('Course.course_id'), nullable=False)
    deadline = Column(DateTime, nullable=False)
    which_week = Column(DateTime, nullable=False)

    course = relationship('Course')


class Content(Base):
    __tablename__ = 'Content'

    content_id = Column(Integer, primary_key=True)
    course_id = Column(ForeignKey('Course.course_id'), nullable=False)
    content_type = Column(String, nullable=False)
    url = Column(String, unique=True)
    transcript_url = Column(String, unique=True)

    course = relationship('Course')


class CourseStudent(Base):
    __tablename__ = 'Course_student'

    id = Column(Integer, primary_key=True)
    student_id = Column(ForeignKey('Student.student_id'))
    course_id = Column(ForeignKey('Course.course_id'))

    course = relationship('Course')
    student = relationship('Student')


class InstructorCourse(Base):
    __tablename__ = 'Instructor_course'

    id = Column(Integer, primary_key=True)
    course_id = Column(ForeignKey('Course.course_id'))
    instructor_id = Column(ForeignKey('Instructor.instructor_id'))

    course = relationship('Course')
    instructor = relationship('Instructor')


class User(Base):
    __tablename__ = 'User'

    user_id = Column(Integer, primary_key=True)
    fs_uniquifier = Column(String, nullable=False, unique=True)
    email = Column(ForeignKey('Student.email'), ForeignKey('Instructor.email'), nullable=False, unique=True)

    Student = relationship('Student', uselist=False)
    Instructor = relationship('Instructor', uselist=False)


class AssignmentStudent(Base):
    __tablename__ = 'Assignment_student'

    id = Column(Integer, primary_key=True)
    assignment_id = Column(ForeignKey('Assignment.assignment_id'), ForeignKey('Student.student_id'))
    student_id = Column(Integer)
    marks_answers = Column(String, nullable=False)

    assignment = relationship('Assignment')
    assignment1 = relationship('Student')


class Question(Base):
    __tablename__ = 'Question'

    question_id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    assignment_id = Column(ForeignKey('Assignment.assignment_id'), nullable=False)
    question = Column(String, nullable=False)
    options = Column(String)
    correct_options = Column(String, nullable=False)
    marks = Column(Integer, nullable=False)
    hints = Column(String)
    text_solution = Column(String)

    assignment = relationship('Assignment')


class UserRole(Base):
    __tablename__ = 'User_role'

    id = Column(Integer, primary_key=True)
    role_id = Column(ForeignKey('Role.role_id'), nullable=False)
    user_id = Column(ForeignKey('User.user_id'), nullable=False)

    role = relationship('Role')
    user = relationship('User')
