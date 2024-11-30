from flask import Blueprint, request, jsonify, render_template
from services.adoption_service import AdoptionService

adoption_bp = Blueprint("adoption", __name__)
adoption_service = AdoptionService()

@adoption_bp.route("/adoption/browse", methods=["GET"])
def browse_pets():
    try:
        pets = adoption_service.get_available_pets()
        return jsonify({"pets": pets}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@adoption_bp.route("/adoption/view/<int:pet_id>", methods=["GET"])
def view_pet(pet_id):
    try:
        pet = adoption_service.get_pet_profile(pet_id)
        if pet:
            return jsonify({"pet": pet}), 200
        return jsonify({"message": "Pet not found."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@adoption_bp.route("/adoption/quiz/<string:username>/<int:pet_id>", methods=["POST"])
def take_adoption_quiz(username, pet_id):
    try:
        quiz_answers = request.json.get("quiz_answers", [])
        quiz_result = adoption_service.take_adoption_quiz(quiz_answers)
        if quiz_result:
            adoption_service.submit_adoption_request(username, pet_id, quiz_result)
            return jsonify({"message": "Adoption request approved!"}), 200
        return jsonify({"message": "Adoption request denied. Please try again."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@adoption_bp.route("/adoption/status/<string:username>", methods=["GET"])
def check_status(username):
    try:
        status = adoption_service.get_adoption_status(username)
        return jsonify({"status": status}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
