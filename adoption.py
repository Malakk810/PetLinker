from flask import Blueprint, request, jsonify
from services.adoptionServices import AdoptionService

adoption_bp = Blueprint("adoption", __name__)
adoption_service = AdoptionService()

# Route to browse pets for adoption
@adoption_bp.route('/pets', methods=['GET'])
def browse_pets_for_adoption():
    pets = adoption_service.get_all_pets()
    return jsonify(pets)

# Route to view pet profile
@adoption_bp.route('/pets/<int:pet_id>', methods=['GET'])
def view_pet_profile(pet_id):
    pet = adoption_service.get_pet_by_id(pet_id)
    if pet:
        return jsonify(pet)
    return jsonify({"error": "Pet not found"}), 404

# Route to submit adoption request
@adoption_bp.route('/adopt', methods=['POST'])
def submit_adoption_request():
    data = request.json
    pet_id = data.get("pet_id")
    username = data.get("username")
    answers = data.get("answers")  # This is the list of answers from the quiz

    # Submit the adoption request only if the user passed the quiz
    result = adoption_service.submit_adoption_request(pet_id, username, answers)
    return jsonify(result)

# Route to check adoption status updates
@adoption_bp.route('/adoption-status/<int:adopter_id>', methods=['GET'])
def adoption_status_updates(adopter_id):
    updates = adoption_service.get_adoption_updates(adopter_id)
    if updates:
        return jsonify({"updates": updates})
    return jsonify({"message": "No new updates"})
