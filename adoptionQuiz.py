from flask import Blueprint, request, jsonify
from services.adoptionQuizService import AdoptionService

adoption_bp = Blueprint("adoption", __name__)
adoption_service = AdoptionService()

@adoption_bp.route("/adoption/quiz/<string:username>", methods=["POST"])
def adoption_quiz(username):
    quiz_result = adoption_service.ask_adoption_quiz(username, request.json.get("answers", []))
    if quiz_result:
        return jsonify({"message": "Congratulations! You passed the adoption quiz."}), 200
    return jsonify({"message": "Sorry, you did not pass the adoption quiz."}), 400

@adoption_bp.route("/adoption/decision/<string:username>", methods=["POST"])
def adoption_decision(username):
    decision = request.json.get("decision")
    if decision.lower() == "yes":
        quiz_passed = adoption_service.choose_adoption(username)
        return jsonify({"message": "Adoption quiz taken.", "quiz_result": quiz_passed}), 200
    return jsonify({"message": "Adoption declined by user."}), 200