from application.extensions import db
from application.models import Instructor, Student

def create_data(datastore):
    datastore.find_or_create_role(name='instructor', description='This is instructor role')
    datastore.find_or_create_role(name='ta', description='This is ta role')
    datastore.find_or_create_role(name='student', description='This is student role')

    if not datastore.find_user(email='test_instructor@gmail.com'):
        user = datastore.create_user(email='test_instructor@gmail.com', active=True, roles=['instructor'])
        db.session.flush()
        instructor = Instructor(name="Test Instructor", email=user.email)
        db.session.add(instructor)

    if not datastore.find_user(email='test_ta@gmail.com'):
        user = datastore.create_user(email='test_ta@gmail.com', active=True, roles=['ta', 'student'])
        db.session.flush()
        instructor = Student(student_name="Test TA", email=user.email)
        db.session.add(instructor)

    if not datastore.find_user(email='test_student@gmail.com'):
        user = datastore.create_user(email='test_student@gmail.com', active=True, roles=['student'])
        db.session.flush() 
        student = Student(student_name="Test Student", email=user.email)
        db.session.add(student)
        
    db.session.commit()
