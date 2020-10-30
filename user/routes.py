from flask import Flask, render_template, Blueprint, session, redirect, url_for
from functools import wraps
from user.models import User

user = Blueprint('user', __name__)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')
    return wrap

@user.route('/user/signup', methods=['POST'])
def signup():
    return User().signup()

@user.route('/user/signout/')
def signout():
    return User().signout()

@user.route('/dashboard/')
@login_required
def dashboard():
    image_file = url_for('static', filename='images/' + session['user'].get('profile_pic'))
    return render_template('dashboard.html', image_file=image_file)
