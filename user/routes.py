from flask import Flask, render_template, Blueprint, session, redirect
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
    return render_template('dashboard.html')
