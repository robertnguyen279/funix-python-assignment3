import os
from flask import Flask, render_template, jsonify
from src.routes import routes_page
from src.models import login_manager
from flask_migrate import Migrate
from src.models import db
from flask_jwt_extended import JWTManager

# Initialize app
app  = Flask(__name__)

# App configs
app.config['SECRET_KEY'] = 'funix-assignment3'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db, migrate & Jwt
db.init_app(app)
Migrate(app,db)
jwt = JWTManager(app)

# Init login manager
login_manager.init_app(app)
login_manager.login_view = "routes.login"

# Register routes
app.register_blueprint(routes_page)

# Register 404 page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404