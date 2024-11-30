from flask import Blueprint, request, jsonify
from services.adoptionServices import AdoptionService

adoption_bp = Blueprint("adoption", __name__)
adoption_service = AdoptionService()

# Function to check user login or signup
def user_profile():
    return {"message": "Please login or signup to access this service."}

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
    quiz_result = data.get("quiz_result")

    result = adoption_service.submit_adoption_request(pet_id, username, quiz_result)
    return jsonify(result)

# Route to check adoption status updates
@adoption_bp.route('/adoption-status/<int:adopter_id>', methods=['GET'])
def adoption_status_updates(adopter_id):
    updates = adoption_service.get_adoption_updates(adopter_id)
    if updates:
        return jsonify({"updates": updates})
    return jsonify({"message": "No new updates"})

