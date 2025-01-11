from flask import request, jsonify, flash, redirect, url_for
from flask_restful import Resource, Api
from werkzeug.security import generate_password_hash, check_password_hash
from blog import db, bcrypt
from blog.models import User
from flask_login import login_user, logout_user, login_required


class UserRegisterResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return jsonify({'message': 'Missing required fields'}), 400
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            return jsonify({'message': 'User already exists'}), 400
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'Account created successfully'}), 201

class UserLoginResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'message': 'Missing required fields'}), 400
        
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return jsonify({'message': 'Login successful'}), 200
        
        return jsonify({'message': 'Login failed. Check your email and password'}), 401

class LogoutResource(Resource):
    @login_required
    def post(self):
        logout_user()
        return jsonify({'message': 'You have been logged out'}), 200
