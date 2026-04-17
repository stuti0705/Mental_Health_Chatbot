from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from database.models import User
from extensions import db
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    hashed_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

    new_user = User(
        name=data['name'],
        email=data['email'],
        password=hashed_pw
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"})


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    user = User.query.filter_by(email=data['email']).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "message": "Login successful",
        "access_token": access_token
    })
