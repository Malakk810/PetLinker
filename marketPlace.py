from flask import Blueprint, request, jsonify
from services.marketplace_service import MarketplaceService

marketplace_bp = Blueprint('marketplace', __name__)
marketplace_service = MarketplaceService()

@marketplace_bp.route('/initialize', methods=['POST'])
def initialize():
    marketplace_service.initialize_database()
    marketplace_service.insert_sample_data()
    return jsonify({"message": "Marketplaces table initialized with sample data."}), 201

@marketplace_bp.route('/', methods=['GET'])
def get_marketplaces():
    location = request.args.get('location', '').strip()

    marketplaces = marketplace_service.get_pet_marketplaces(location)
    if isinstance(marketplaces, str):  # Error message
        return jsonify({"message": marketplaces}), 404
    return jsonify(marketplaces), 200
