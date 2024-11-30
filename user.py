from flask import Blueprint, request, jsonify
from services.user_service import UserService

user_bp = Blueprint("user", __name__)
user_service = UserService()

@user_bp.route("/create_user", methods=["POST"])
def create_user():
    return user_service.create_user(request.json)

@user_bp.route("/edit_user/<username>", methods=["PUT"])
def edit_user_profile(username):
    return user_service.edit_user_profile(username, request.json)

@user_bp.route("/delete_user/<username>", methods=["DELETE"])
def delete_user_profile(username):
    return user_service.delete_user_profile(username)
