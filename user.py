from flask import Blueprint, request, render_template, redirect, url_for, flash
from services.user_service import UserService

user_bp = Blueprint("user", __name__)
user_service = UserService()

@user_bp.route("/create_user", methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        data = request.form.to_dict()
        pet_data = None
        if data.get('pet') == 'Yes':
            pet_data = {
                "age": data.get('age'),
                "location": data.get('location'),
                "breed": data.get('breed'),
                "history": data.get('history')
            }
        return user_service.create_user(data, pet_data)
    return render_template("create_user.html")

@user_bp.route("/edit_user/<username>", methods=["GET", "POST"])
def edit_user_profile(username):
    if request.method == "POST":
        data = request.form.to_dict()
        pet_data = None
        if data.get('pet') == 'Yes':
            pet_data = {
                "age": data.get('age'),
                "location": data.get('location'),
                "breed": data.get('breed'),
                "history": data.get('history')
            }
        return user_service.edit_user_profile(username, data, pet_data)
    return render_template("edit_user.html", username=username)

@user_bp.route("/delete_user/<username>", methods=["POST"])
def delete_user_profile(username):
    return user_service.delete_user_profile(username)
