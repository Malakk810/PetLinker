from flask import Blueprint, request, jsonify   #import flask tools
from services.user_service import UserService   #import class container
#user is the container for all routes
user= Blueprint('user', __name__)  #group routes
user_service = UserService()  #class handle all business logic & user actions

@user.route("/user/register", methods=["POST"])    #route that handles post requests
def register_user():
    data = request.json  #extract the data from the request body
    result = user_service.create_user(data)   #authenticate data entered by user
    return jsonify(result), 201 if result["success"] else 400   #201 for POST method

@user.route("/user/login", methods=["POST"])
def login_user():
    data = request.json
    result = user_service.login_user(data)
    return jsonify(result), 200 if result["success"] else 400   #200 for GET method

@user.route("/user/edit/<string:username>", methods=["PUT"])
def edit_user(username):
    data = request.json
    result = user_service.edit_user_profile(username, data)
    return jsonify(result), 200 if result["success"] else 400 #400 for unsuccessful

@user.route("/user/delete/<string:username>", methods=["DELETE"])
def delete_user(username):
    result = user_service.delete_user_profile(username)
    return jsonify(result), 200 if result["success"] else 400



