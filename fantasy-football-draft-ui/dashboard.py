from flask import Blueprint, render_template, session

dashboard = Blueprint('dashboard',
                         __name__, 
                        template_folder='templates',
                        static_folder='static', 
                        static_url_path='')

@dashboard.route('/')
def index():
    return render_template('base.html')

