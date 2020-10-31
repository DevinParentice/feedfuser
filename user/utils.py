import os
import secrets
from flask import current_app, session
from PIL import Image
from user.models import db


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path, 'static/images', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    currentUser = db.users.find_one({'username': session['user']['username']})

    prev_picture = os.path.join(
        current_app.root_path, 'static/images', currentUser['profile_pic'])
    if os.path.exists(prev_picture) and os.path.basename(prev_picture) != 'profile.png':
        os.remove(prev_picture)

    return picture_fn
