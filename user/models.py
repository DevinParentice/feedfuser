from flask import Flask, jsonify, request
from flask import jsonify
from flask import jsonify
from passlib.hash import pbkdf2_sha256
import pymongo
import uuid

client = pymongo.MongoClient('localhost', 27017)
db = client.user_login_system

class User:
    
    def signup(self):
        password = request.form.get('password')
        password_confirm = request.form.get('password-confirm')
        
        if password == password_confirm:
            user = {
				"_id": uuid.uuid4().hex,
				"username": request.form.get('username'),
				"email": request.form.get('email'),
				"password": password,
			}
            
            user['password'] = pbkdf2_sha256.encrypt(user['password'])
            
            if db.users.find_one({"email": user['email']}):
                return jsonify({"error": "Email address already in use"}), 400
            
            if db.users.insert_one(user):
            	return jsonify(user), 200
         
        elif password != password_confirm:
            return jsonify({"error": "Passwords do not match, please try again"}), 400
        else:
            return jsonify({"error": "Signup failed"}), 400