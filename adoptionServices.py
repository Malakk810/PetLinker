class AdoptionService:
    def __init__(self):
        # Mock database structure
        self.db = Database()  # Use your database implementation

    def get_available_pets(self):
        query = "SELECT * FROM pets WHERE status = 'Available'"
        pets = self.db.fetch_all(query)
        return pets

    def get_pet_profile(self, pet_id):
        query = "SELECT * FROM pets WHERE pet_id = ?"
        pet = self.db.fetch_one(query, [pet_id])
        return pet

    def take_adoption_quiz(self, answers):
        # Mock quiz logic
        correct_answers = [2, 3, 1, 2]  # Example correct answers
        score = sum(1 for i, answer in enumerate(answers) if answer == correct_answers[i])
        return score >= 3

    def submit_adoption_request(self, username, pet_id, quiz_result):
        if quiz_result:
            # Update pet status
            self.db.execute("UPDATE pets SET status = 'Adopted' WHERE pet_id = ?", [pet_id])
            # Update user adoption status
            self.db.execute("UPDATE users SET adoption_status = 'Adopter' WHERE username = ?", [username])

    def get_adoption_status(self, username):
        query = "SELECT adoption_status FROM users WHERE username = ?"
        status = self.db.fetch_one(query, [username])
        return status if status else "No adoption status available."
