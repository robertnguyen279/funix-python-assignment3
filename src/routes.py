from flask import Blueprint, render_template, send_from_directory

routes_page = Blueprint('routes', __name__, template_folder='templates')

@routes_page.route('/')
def index():
    return render_template('index.html')


# Serve static files
@routes_page.route('/statics/<path:path>')
def send_report(path):
    return send_from_directory('statics', path)