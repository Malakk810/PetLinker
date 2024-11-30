import pyodbc

class AdoptionService:
    def __init__(self):
        self.conn = pyodbc.connect(
            'DRIVER={ODBC Driver 18 for SQL Server};'
            'SERVER=FaridaAli\\SQLEXPRESS;'
            'DATABASE=PetLinker;'
            'UID=flask_user;'
            'PWD=Flask!User1234;'
            'TrustServerCertificate=yes'
        )
        self.cursor = self.conn.cursor()

    def get_all_pets(self):
        self.cursor.execute("SELECT pet_id, name, breed, status FROM pets WHERE status='Available'")
        pets = self.cursor.fetchall()
        return [{"id": row[0], "name": row[1], "breed": row[2]} for row in pets]

    def get_pet_by_id(self, pet_id):
        self.cursor.execute("SELECT * FROM pets WHERE pet_id=?", pet_id)
        pet = self.cursor.fetchone()
        if pet:
            return {
                "id": pet[0],
                "name": pet[1],
                "breed": pet[2],
                "age": pet[3],
                "status": pet[4]
            }
        return None

    def submit_adoption_request(self, pet_id, username, quiz_result):
        if quiz_result:
            self.cursor.execute("UPDATE pets SET status='Adopted' WHERE pet_id=?", pet_id)
            self.cursor.execute("UPDATE UserProfile SET status='Adopter' WHERE username=?", username)
            self.conn.commit()
            return {"message": "Adoption request approved!"}
        return {"message": "Adoption request rejected"}, 400

    def get_adoption_updates(self, adopter_id):
        self.cursor.execute("SELECT * FROM adoption_updates WHERE adopter_id=?", adopter_id)
        updates = self.cursor.fetchall()
        if updates:
            return [{"update_id": row[0], "message": row[1], "date": row[2]} for row in updates]
        return []
