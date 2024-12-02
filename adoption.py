from flask import Blueprint, request, jsonify
from adoptionServices import AdoptionService
from adoptionQuizService import AdoptionQuizService

adoption_bp = Blueprint("adoption", __name__)
adoption_service = AdoptionService()
adoptionQuizService = AdoptionQuizService()

@adoption_bp.route('/pets', methods=['POST'])
def browse_pets_for_adoption():
    # pets = adoption_service.get_all_pets()
    # return jsonify(pets)
    return "Pets" 

@adoption_bp.route('/pets/<int:pet_id>', methods=['GET'])
def view_pet_profile(pet_id):
    pet = adoption_service.get_pet_by_id(pet_id)
    if pet:
        return jsonify(pet)
    return jsonify({"error": "Pet not found"}), 404

@adoption_bp.route('/adopt', methods=['POST'])
def submit_adoption_request():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid data format"}), 400

    pet_id = data.get("pet_id")
    username = data.get("username")
    answers = data.get("answers")

    if not pet_id or not username or answers is None:
        return jsonify({"error": "Missing required fields"}), 400

    result = adoption_service.submit_adoption_request(pet_id, username, answers)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result)

@adoption_bp.route('/adoption-status/<int:adopter_id>', methods=['GET'])
def adoption_status_updates(adopter_id):
    updates = adoption_service.get_adoption_updates(adopter_id)
    if updates:
        return jsonify({"updates": updates})
    return jsonify({"message": "No new updates"})

@adoption_bp.route("/adoption/decision/<string:username>", methods=["POST"])
def adoption_decision(username):
    decision = request.json.get("decision")
    if decision.lower() == "yes":
        quiz_passed = adoptionQuizService.choose_adoption(username)
        return jsonify({"message": "Adoption quiz taken.", "quiz_result": quiz_passed}), 200
    return jsonify({"message": "Adoption declined by user."}), 200
