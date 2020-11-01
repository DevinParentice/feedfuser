import twitter
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
    api = twitter.Api(consumer_key=currentUser['twitter-consumer_key'],
                      consumer_secret=currentUser['twitter-consumer_secret'],
                      access_token_key=currentUser['twitter-access_token_key'],
                      access_token_secret=currentUser['twitter-access_token_secret'])
    statuses = api.GetHomeTimeline()
    tweets = [
        f'https://twitter.com/placeholder/status/{s.id_str}' for s in statuses]
    return render_template('feed.html', feed=tweets)
