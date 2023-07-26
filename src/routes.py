from flask import Blueprint, render_template, send_from_directory, request, flash, redirect, url_for
from src.forms import RegistrationForm
from src.models import User
from sqlalchemy.exc import SQLAlchemyError

routes_page = Blueprint('routes', __name__, template_folder='templates')

@routes_page.route('/')
def index():
    return render_template('index.html', request_path=request.path)


@routes_page.route('/register', methods=['POST', 'GET'])
def register():
    register_form = RegistrationForm()
    if register_form.validate_on_submit():
        new_user = User(email=register_form.email.data, username=register_form.username.data, password=register_form.password.data)
        try:
            new_user.save()
            return redirect(url_for('routes.login'))
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)
            if error == 'UNIQUE constraint failed: users.email':
                flash('Error: Email has been taken')
            elif error == 'UNIQUE constraint failed: users.username':
                flash('Error: Username has been taken')
            else:
                flash(error)
        
        
    return render_template('register.html', request_path=request.path, form=register_form)

@routes_page.route('/login')
def login():
    return render_template('login.html', request_path=request.path)

# Serve static files
@routes_page.route('/statics/<path:path>')
def send_report(path):
    return send_from_directory('statics', path)