from flask import Blueprint, request, jsonify
from services.user_service import UserService

user_bp = Blueprint('user', __name__)
user_service = UserService()

# User Registration Route (Create new account)
@user_bp.route("/user/register", methods=["POST"])
def register_user():
    data = request.json
    result = user_service.create_user(data)
    return jsonify(result), 201 if result["success"] else 400

# User Login Route
@user_bp.route("/user/login", methods=["POST"])
def login_user():
    data = request.json
    result = user_service.login_user(data)
    return jsonify(result), 200 if result["success"] else 400

# Edit Account Route
@user_bp.route("/user/edit/<string:username>", methods=["PUT"])
def edit_user(username):
    data = request.json
    result = user_service.edit_user_profile(username, data)
    return jsonify(result), 200 if result["success"] else 400

# Delete Account Route
@user_bp.route("/user/delete/<string:username>", methods=["DELETE"])
def delete_user(username):
    result = user_service.delete_user_profile(username)
    return jsonify(result), 200 if result["success"] else 400



