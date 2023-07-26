import os
from flask import Flask
from src.routes import routes_page
from src.models import login_manager
from flask_migrate import Migrate
from src.models import db



app  = Flask(__name__)

app.config['SECRET_KEY'] = 'funix-assignment3'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
Migrate(app,db)

login_manager.init_app(app)

login_manager.login_view = "login"

app.register_blueprint(routes_page)