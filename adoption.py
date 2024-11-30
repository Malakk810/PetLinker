from flask import Blueprint, request, jsonify, render_template
from services.adoption_service import AdoptionService

adoption_bp = Blueprint("adoption", __name__)
adoption_service = AdoptionService()

@adoption_bp.route("/")
def main():
    return render_template("login.html")  # Render login/signup page

@adoption_bp.route("/browse_pets", methods=["GET"])
def browse_pets():
    pets = adoption_service.get_available_pets()
    return render_template("browse_pets.html", pets=pets)

@adoption_bp.route("/view_pet/<int:pet_id>", methods=["GET", "POST"])
def view_pet_profile(pet_id):
    if request.method == "GET":
        pet_details = adoption_service.get_pet_profile(pet_id)
        return render_template("pet_profile.html", pet=pet_details)
    elif request.method == "POST":
        quiz_result = adoption_service.take_adoption_quiz(request.json.get("quiz_answers"))
        if quiz_result:
            adoption_service.submit_adoption_request(request.json.get("username"), pet_id, quiz_result)
            return jsonify({"message": "Adoption request approved!"}), 200
        return jsonify({"message": "Adoption request denied. Please try again."}), 400
