from flask import Blueprint, render_template, send_from_directory, request, flash, redirect, url_for
from src.forms import RegistrationForm, LoginForm, AddTodoForm, EditTodoForm
from src.models import User, Todo
from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_user,login_required,logout_user
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask import request
from flask import jsonify

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
            if error == 'UNIQUE constraint failed: users.email':
                flash('Error: Email has been taken')
            elif error == 'UNIQUE constraint failed: users.username':
                flash('Error: Username has been taken')
            else:
                flash(error)
    
    return render_template('register.html', request_path=request.path, form=register_form)

@routes_page.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user is not None and user.check_password(login_form.password.data):
            login_user(user)
            
            next = request.args.get('next')
            if next == None or not next[0]=='/':
                next = url_for('routes.index')

            return redirect(next)
        else:
            flash('Wrong username or password')
    return render_template('login.html', request_path=request.path, form=login_form)


@routes_page.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.index'))

@routes_page.route('/add', methods=['POST', 'GET'])
@login_required
def add_todo():
    add_todo_form = AddTodoForm()
    if add_todo_form.validate_on_submit():
        category = add_todo_form.category.data
        description = add_todo_form.description.data
        new_todo = Todo(category, description)
        try:
            new_todo.save()
            return redirect(url_for('routes.index'))
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            if error == 'UNIQUE constraint failed: todo.category':
                flash('Error: Category already exists')
            else:
                flash(error)
    return render_template('add.html', request_path=request.path, form=add_todo_form)

@routes_page.route('/manage')
@login_required
def manage_todo():
    return render_template('manage.html', request_path=request.path)

@routes_page.route('/edit/<path:id>', methods=['GET', 'POST'])
@login_required
def edit_todo(id):
    todo = Todo.query.get(id)
    edit_form = EditTodoForm()
    if edit_form.validate_on_submit():
        todo.category = edit_form.category.data
        todo.description = edit_form.description.data
        todo.status = edit_form.status.data
    
        todo.save()
        return redirect(url_for('routes.manage_todo'))
    return render_template('edit.html', form=edit_form, todo=todo)
    
@routes_page.route('/delete/<path:id>')
@login_required
def delete_todo(id):
    todo = Todo.query.get(id)
    if not todo:
        return render_template('404.html'), 404
    
    todo.delete()
    return redirect(url_for('routes.manage_todo', request_path=request.path))


@routes_page.route("/login-jwt", methods=["POST"])
def login_jwt():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(username=username).first()
    if user is not None and user.check_password(password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)

    else:
        return jsonify({"Message": "Wrong username or password"}), 401

# Protect a route with jwt_required, which will kick out requests without a valid JWT present.
@routes_page.route("/todos", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    todos = Todo.query.filter_by(user_id=user.id).all()
    if not todos:
        return jsonify({"Message": "No todo found"}), 404
    

    formatted_todos = [todo.json() for todo in todos]
    return formatted_todos, 200

# Serve static files
@routes_page.route('/statics/<path:path>')
def send_report(path):
    return send_from_directory('statics', path)

