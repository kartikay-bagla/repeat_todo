import json

from flask import Blueprint, jsonify, request
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from repeat_todo.extensions import db
from repeat_todo.models.user import User

auth_route = Blueprint("auth", __name__)


@auth_route.route("/signup", methods=["POST"])
def signup():
    """Signup a new user."""
    data = json.loads(request.data)

    try:
        username = data["username"]
        password = data["password"]
        name = data["name"]
    except KeyError:
        return jsonify({"error": "Missing username, password or name"}), 400

    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({"error": "Username already exists"}), 400

    hashed_password = generate_password_hash(password, method='sha256')

    new_user = User(username=username, password=hashed_password, name=name)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully."})


@auth_route.route("/login", methods=["POST"])
def login():
    """Login a user."""
    data = json.loads(request.data)

    try:
        username = data["username"]
        password = data["password"]
    except KeyError:
        return jsonify({"error": "Missing username or password"}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "Username does not exist"}), 400

    if not check_password_hash(user.password, password):
        return jsonify({"error": "Incorrect password"}), 400

    login_user(user)
    return jsonify({"message": "User logged in successfully."})


@auth_route.route("/logout", methods=["POST"])
@login_required
def logout():
    """Logout a user."""
    logout_user()
    return jsonify({"message": "User logged out successfully."})
