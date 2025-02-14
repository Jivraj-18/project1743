from application.extensions import db
from application.models import Instructor, Student

def create_data(datastore):
    datastore.find_or_create_role(name='instructor', description='This is instructor role')
    datastore.find_or_create_role(name='ta', description='This is ta role')
    datastore.find_or_create_role(name='student', description='This is student role')

    if not datastore.find_user(email='test_instructor@study.iitm.ac.in'):
        user = datastore.create_user(email='test_instructor@study.iitm.ac.in', active=True, roles=['instructor'])
        db.session.flush()
        instructor = Instructor(name="Test Instructor", email=user.email)
        db.session.add(instructor)

    if not datastore.find_user(email='test_ta@ds.study.iitm.ac.in'):
        user = datastore.create_user(email='test_ta@ds.study.iitm.ac.in', active=True, roles=['ta'])
        db.session.flush()
        instructor = Instructor(name="Test TA", email=user.email)
        db.session.add(instructor)

    if not datastore.find_user(email='test_student@ds.study.iitm.ac.in'):
        user = datastore.create_user(email='test_student@ds.study.iitm.ac.in', active=True, roles=['student'])
        db.session.flush() 
        student = Student(student_name="Test Student", email=user.email)
        db.session.add(student)
        
    db.session.commit()
