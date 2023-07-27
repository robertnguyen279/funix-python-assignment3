import os
from flask import Flask, render_template, jsonify
from src.routes import routes_page
from src.models import login_manager
from flask_migrate import Migrate
from src.models import db
from flask_jwt_extended import JWTManager



app  = Flask(__name__)

app.config['SECRET_KEY'] = 'funix-assignment3'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
Migrate(app,db)
jwt = JWTManager(app)



login_manager.init_app(app)

login_manager.login_view = "routes.login"

app.register_blueprint(routes_page)

# Register 404 page
@app.errorhandler(404)
def page_not_found(e):
    # Note that we set the 404 status explicitly
    return render_template('404.html'), 404