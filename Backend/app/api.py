from flask import jsonify, Blueprint, request
from app.models import User
from datetime import datetime, date, timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import select
from sqlalchemy import or_, distinct
from app.database import db

api_bp = Blueprint("api", __name__)


@api_bp.route("/test")
def test():
    return jsonify({"message": "api working"})


@api_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"message": "invalid user"})
    else:
        if check_password_hash(user.password, password):
            token = create_access_token(identity=str(user.id))
            print(f"token: {token}")
            return jsonify(
                {"message": "Login Successful", "token": token, "name": user.username}
            )
        else:
            return jsonify({"message": "Invalid Password"})


@api_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()

        username = data.get("username")
        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        password = data.get("password")

        if not all([username, name, email, password]):
            return (
                jsonify({"message": "Username, name, email and password are required"}),
                400,
            )

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({"message": "Username already exists"}), 409

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            return jsonify({"message": "Email already registered"}), 409

        if phone:
            existing_phone = User.query.filter_by(phone=phone).first()
            if existing_phone:
                return jsonify({"message": "Phone number already registered"}), 409

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        new_user = User(
            username=username,
            name=name,
            email=email,
            phone=phone,
            password=hashed_password,
        )

        db.session.add(new_user)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Registration successful",
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        print(f"Registration Error: {e}")

        return jsonify({"message": "Registration failed"}), 500
