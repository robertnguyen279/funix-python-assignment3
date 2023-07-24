from flask import Flask
from src.routes import routes_page

app  = Flask(__name__)

app.register_blueprint(routes_page)