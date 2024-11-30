from flask import Blueprint, request, jsonify
from services.activity_service import ActivityService

activity_bp = Blueprint('activity', __name__)
activity_service = ActivityService()

@activity_bp.route('/initialize', methods=['POST'])
def initialize():
    activity_service.initialize_database()
    activity_service.insert_sample_activities()
    return jsonify({"message": "Activities table initialized with sample data."}), 201

@activity_bp.route('/', methods=['GET'])
def find_activities():
    location = request.args.get('location', '').strip()
    activity_type = request.args.get('activity_type', '').strip()

    if not location:
        return jsonify({"error": "Location data missing. Please enter a valid location."}), 400

    activities = activity_service.find_pet_activities(location, activity_type)
    if isinstance(activities, str):  # Error message
        return jsonify({"message": activities}), 404
    return jsonify(activities), 200
