from PIL.Image import new
from flask import render_template, Blueprint, session, redirect, url_for, request, jsonify, flash
from functools import wraps

from user.utils import save_picture
from user.models import User, db

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


@user.route('/user/login', methods=['POST'])
def login():
    return User().login()


@user.route('/dashboard/', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        picture = request.files.get('profile-pic')
        newPic = save_picture(picture)
        db.users.update_one(
            {'_id': session['user'].get('_id')},
            {'$set': {"profile_pic": newPic}}
        )
        flash('Profile picture successfully updated', 'success')
        return jsonify({"success": "Profile picture successfully updated"}), 200
    else:
        currentUser = db.users.find_one(
            {'username': session['user']['username']})
        image_file = url_for('static', filename='images/' +
                             currentUser['profile_pic'])
        return render_template('dashboard.html', image_file=image_file)


@user.route('/twitter')
@login_required
def twitter():
    return render_template('twitter.html')
