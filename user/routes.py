from flask import Flask, render_template, Blueprint
from user.models import User

user = Blueprint('user', __name__)

@user.route('/user/signup', methods=['POST'])
def signup():
    return User().signup()