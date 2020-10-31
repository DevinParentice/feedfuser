from flask import render_template, Blueprint, session, redirect, url_for
from functools import wraps
from user.models import db

main = Blueprint('main', __name__)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')
    return wrap


@main.route('/')
@main.route('/home/')
def home():
    if session['logged_in'] == True:
        currentUser = db.users.find_one(
            {'email': session['user']['email']})
        image_file = url_for('static', filename='images/' +
                             currentUser['profile_pic'])
        return render_template('home.html', image_file=image_file)
    return render_template('home.html')


@main.route("/feed/")
@login_required
def feed():
    return render_template('feed.html')
