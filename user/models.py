from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
import pymongo
import uuid

client = pymongo.MongoClient('localhost', 27017)
db = client.user_login_system


class User:

    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200

    def signup(self):
        password = request.form.get('password')
        password_confirm = request.form.get('password-confirm')

        if password == password_confirm:
            if len(password) < 4:
                return jsonify({"error": "Password must be greater than four characters"}), 400
            user = {
                "_id": uuid.uuid4().hex,
                "username": request.form.get('username'),
                "email": request.form.get('email'),
                "password": password,
                "profile_pic": 'profile.png',
                "twitter-consumer_key": "UvIXepn05rKQoEzLICcMMIAyc",
                "twitter-consumer_secret": "V7rQqKqDxmG1qUJ4u8ueOmOSjxSIJ7U62ZmABSTHqt8Ti66OHZ",
                "twitter-access_token_key": "3601558037-dTlQMkcXkEFkTknftc1zKDzz9Rd3PO0HxIwVpCj",
                "twitter-access_token_secret": "MxsHWz0XwHIrv2KJgAWVkxMrCXv0Miu7XXCKPYSGUM4QK"
            }

            user['password'] = pbkdf2_sha256.encrypt(user['password'])
            request.close()
            if db.users.find_one({"email": user['email']}):
                return jsonify({"error": "Email address is already in use, please sign in"}), 400
            elif db.users.find_one({"username": user['username']}):
                return jsonify({"error": "Username is already in use, please choose another"}), 400

            if db.users.insert_one(user):
                return self.start_session(user)

        elif password != password_confirm:
            return jsonify({"error": "Passwords do not match, please try again"}), 400
        else:
            return jsonify({"error": "Signup failed"}), 400

    def signout(self):
        session.clear()
        return redirect('/')

    def login(self):
        user = db.users.find_one({
            "email": request.form.get('email')
        })

        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)
        return jsonify({"error": "Invalid login credentials"}), 401
