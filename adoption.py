from flask import Blueprint, request, jsonify
import pyodbc

adoption_bp = Blueprint("adoption", __name__)

# Establish database connection
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 18 for SQL Server};'
    'SERVER=FaridaAli\\SQLEXPRESS;'
    'DATABASE=PetLinker;'
    'UID=flask_user;'
    'PWD=Flask!User1234;'
    'TrustServerCertificate=yes'
)
cursor = conn.cursor()

# Function to check user login or signup
def user_profile():
    return {"message": "Please login or signup to access this service"}

# Route to browse pets for adoption
@adoption_bp.route('/pets', methods=['GET'])
def browse_pets_for_adoption():
    cursor.execute("SELECT pet_id, name, breed, status FROM pets WHERE status='Available'")
    pets = cursor.fetchall()
    pet_list = [{"id": row[0], "name": row[1], "breed": row[2]} for row in pets]
    return jsonify(pet_list)

# Route to view pet profile
@adoption_bp.route('/pets/<int:pet_id>', methods=['GET'])
def view_pet_profile(pet_id):
    cursor.execute("SELECT * FROM pets WHERE pet_id=?", pet_id)
    pet = cursor.fetchone()
    if pet:
        pet_details = {
            "id": pet[0],
            "name": pet[1],
            "breed": pet[2],
            "age": pet[3],
            "status": pet[4]
        }
        return jsonify(pet_details)
    return jsonify({"error": "Pet not found"}), 404

# Route to submit adoption request
@adoption_bp.route('/adopt', methods=['POST'])
def submit_adoption_request():
    data = request.json
    pet_id = data.get("pet_id")
    username = data.get("username")
    quiz_result = data.get("quiz_result")

    if quiz_result:
        # Approve request and update status
        cursor.execute("UPDATE pets SET status='Adopted' WHERE pet_id=?", pet_id)
        cursor.execute("UPDATE UserProfile SET status='Adopter' WHERE username=?", username)
        conn.commit()
        return jsonify({"message": "Adoption request approved!"})
    return jsonify({"message": "Adoption request rejected"}), 400

# Route to check adoption status updates
@adoption_bp.route('/adoption-status/<int:adopter_id>', methods=['GET'])
def adoption_status_updates(adopter_id):
    cursor.execute("SELECT * FROM adoption_updates WHERE adopter_id=?", adopter_id)
    updates = cursor.fetchall()
    if updates:
        return jsonify({"message": "New adoption status updates available", "updates": updates})
    return jsonify({"message": "No new updates"})
