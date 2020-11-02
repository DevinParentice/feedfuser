import twitter
import pytz
from datetime import date, datetime
from instagram_private_api import Client, ClientCompatPatch
from flask import render_template, Blueprint, session, redirect, url_for
from functools import wraps
from user.models import db
from main.utils import login_twitter, ig_login

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
    if 'logged_in' in session:
        currentUser = db.users.find_one(
            {'email': session['user']['email']})
        image_file = url_for('static', filename='images/' +
                             currentUser['profile_pic'])
        return render_template('home.html', image_file=image_file)
    return render_template('home.html')


@main.route("/feed/")
@login_required
def feed():
    currentUser = db.users.find_one(
        {'email': session['user']['email']})
    tweets = login_twitter(currentUser)
    ig_pics = ig_login(currentUser)
    total_feed = tweets + ig_pics
    total_feed.sort(key=lambda x: x['Date'], reverse=True)
    return render_template('feed.html', feed=total_feed)
