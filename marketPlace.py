from flask import Blueprint, request, jsonify
from marketplaceServices import MarketplaceService

# Create the blueprint for marketplace routes
marketplace_bp = Blueprint("marketplace", __name__)
marketplace_service = MarketplaceService()

@marketplace_bp.route("/marketplaces", methods=["GET"])
def get_all_pet_marketplaces():
    # Get location from query parameters
    location = request.args.get('location')

    # Get the pet marketplaces from the service
    marketplaces = marketplace_service.get_pet_marketplaces(location)

    if isinstance(marketplaces, str):  # Error message case
        return jsonify({"message": marketplaces}), 404

    return jsonify(marketplaces)

@marketplace_bp.route("/marketplaces/sample", methods=["POST"])
def insert_sample_marketplaces():
    try:
        # Insert the sample data into the database
        marketplace_service.insert_sample_data()
        return jsonify({"message": "Sample pet marketplaces inserted successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
