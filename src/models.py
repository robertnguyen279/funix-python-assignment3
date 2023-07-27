from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from datetime import date

login_manager = LoginManager()

db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    # Create a table in the db
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    todos = db.relationship('Todo', backref='user', lazy='dynamic')

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

class Todo(db.Model, UserMixin):

    __table_name__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(255))
    status = db.Column(db.String(64))
    date_created = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, category, description):
        self.category = category
        self.description = description
        self.status = "pending"
        self.date_created = date.today()
        self.user_id = current_user.id
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def json(self):
        return {
            "category": self.category,
            "description": self.description,
            "status": self.status,
            "date_created": self.date_created
        }

