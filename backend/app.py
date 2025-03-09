from flask import Flask
from application.extensions import db, security
import init_db
import application.views as views
from flask_security import SQLAlchemyUserDatastore
from application.resources import api
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'mysecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECURITY_PASSWORD_SALT'] = 'mysaltypassword'
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = 'Authentication'

    db.init_app(app)

    with app.app_context():
        from application.models import User, Role, Base

        datastore = SQLAlchemyUserDatastore(db, User, Role)
        security.init_app(app, datastore)
        
        try:
            print("Creating all tables in the database...")
            Base.metadata.create_all(db.engine)  
        except Exception as e:
            print(f"Error while creating tables: {e}")

        init_db.create_data(datastore)

    views.create_view(app, datastore, db)
    api.init_app(app)
    return app


app = create_app()
CORS(app)

if __name__ == '__main__':
    app.run()
