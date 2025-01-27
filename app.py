from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.vxvglefymtcqlvylhnxj:dtl7FbAlLsVOYghU@aws-0-ap-northeast-2.pooler.supabase.com:6543/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import models here
from model import *  # Ensure your models are defined in the 'model' module

@app.before_request
def create_tables():
    db.create_all()  # This will create all tables

@app.route('/')
def index():
    new_course = Course(name="Introduction to Python", description="Learn Python basics.")
    db.session.add(new_course)
    db.session.commit()
    return "Hello, World!"

if __name__ == "__main__":
    app.run()