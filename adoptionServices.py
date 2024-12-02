import pyodbc
from services.adoptionQuizService import AdoptionQuizService

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
        self.quiz_service = AdoptionQuizService()

    def get_all_pets(self):
        self.cursor.execute("""
            SELECT Licence_number, Gender, Age, Health_Condition, Type_, Status_, Location 
            FROM pets 
            WHERE Status_ = 'Available'
        """)
        pets = self.cursor.fetchall()
        return [
            {"Licence_number": row[0], "Gender": row[1], "Age": row[2], "Health_condition": row[3], 
             "Type_": row[4], "Status_": row[5], "Location": row[6]} for row in pets
        ]

    def get_pet_by_id(self, pet_id):
        self.cursor.execute("SELECT * FROM pets WHERE Licence_number=?", pet_id)
        pet = self.cursor.fetchone()
        if pet:
            return {
                "Licence_number": pet[0],
                "Gender": pet[1],
                "Age": pet[2],
                "Health_condition": pet[3],
                "Type_": pet[4],
                "Status_": pet[5]
            }
        return None

    def submit_adoption_request(self, pet_id, username, answers):
        quiz_result = self.quiz_service.ask_adoption_quiz(self, username, answers))
        if quiz_result:
            self.cursor.execute("UPDATE Pets SET Status_='Adopted' WHERE Licence_number=?", pet_id)
            self.cursor.execute("UPDATE UserProfiles SET status='Adopter' WHERE username=?", username)
            self.conn.commit()
            return {"message": "Adoption request approved!"}
        else:
            return {"message": "Adoption request rejected. Please pass the quiz to adopt."}, 400

    def get_adoption_updates(self, adopter_id):
        self.cursor.execute("SELECT * FROM adoption_updates WHERE username=?", adopter_id)
        updates = self.cursor.fetchall()
        if updates:
            return [{"update_id": row[0], "message": row[1], "date": row[2]} for row in updates]
        return []
