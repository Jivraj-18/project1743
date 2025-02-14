from flask import render_template, Flask, request, jsonify, render_template_string, send_file
from flask_security import SQLAlchemyUserDatastore
from flask_security import logout_user, current_user, auth_token_required, roles_accepted

def create_view(app : Flask, datastore : SQLAlchemyUserDatastore, db):
    @app.route('/')
    def home():
        return render_template('login.html')