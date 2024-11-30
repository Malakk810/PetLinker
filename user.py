from flask import Blueprint, request, jsonify
from services.user_service import UserService

user_bp = Blueprint("user", __name__)
user_service = UserService()

@user_bp.route("/user/create", methods=["POST"])
def create_user():
    try:
        user_data = request.json  # Receive user data as JSON
        result = user_service.create_user(user_data)
        if result["success"]:
            return jsonify({"message": result["message"]}), 201
        return jsonify({"message": result["message"]}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user_bp.route("/user/edit/<string:username>", methods=["PUT"])
def edit_user(username):
    try:
        update_data = request.json  # Receive update data as JSON
        result = user_service.edit_user_profile(username, update_data)
        if result["success"]:
            return jsonify({"message": result["message"]}), 200
        return jsonify({"message": result["message"]}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user_bp.route("/user/delete/<string:username>", methods=["DELETE"])
def delete_user(username):
    try:
        result = user_service.delete_user_profile(username)
        if result["success"]:
            return jsonify({"message": result["message"]}), 200
        return jsonify({"message": result["message"]}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
