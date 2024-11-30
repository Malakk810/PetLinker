from flask import Blueprint, request, jsonify
from services.pet_activity_service import PetActivityService

# Create the blueprint for pet activity routes
pet_activity_bp = Blueprint("pet_activity", __name__)
activity_service = PetActivityService()

@pet_activity_bp.route("/activities", methods=["GET"])
def get_pet_activities():
    location = request.args.get('location')  # Get location from query parameters
    activity_type = request.args.get('activity_type')  # Optionally filter by activity type

    # Fetch pet activities from the service
    activities = activity_service.find_pet_activities(location, activity_type)
    
    # Check if the result is an error message
    if isinstance(activities, str):  # If it’s an error message
        return jsonify({"message": activities}), 404
    
    return jsonify(activities)

@pet_activity_bp.route("/activities/upcoming", methods=["GET"])
def get_upcoming_events():
    location = request.args.get('location')  # Get location from query parameters

    if not location:
        return jsonify({"message": "Location is required to get upcoming events."}), 400

    # Fetch upcoming events from the service
    events = activity_service.find_upcoming_events(location)
    
    if isinstance(events, str):  # If it’s an error message
        return jsonify({"message": events}), 404
    
    return jsonify(events)

@pet_activity_bp.route("/activities/sample", methods=["POST"])
def insert_sample_activities():
    # Insert the sample data into the database
    activity_service.insert_sample_activities()
    return jsonify({"message": "Sample pet activities inserted successfully!"}), 201
