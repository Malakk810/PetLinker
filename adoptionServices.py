class AdoptionService:
    def __init__(self):
        # Mock database structure
        self.pets = [
            {"id": 1, "name": "Buddy", "type": "Dog", "status": "Available"},
            {"id": 2, "name": "Mittens", "type": "Cat", "status": "Available"},
        ]
        self.users = {}

    def get_available_pets(self):
        return [pet for pet in self.pets if pet["status"] == "Available"]

    def get_pet_profile(self, pet_id):
        for pet in self.pets:
            if pet["id"] == pet_id:
                return pet
        return None

    def take_adoption_quiz(self, answers):
        # Example logic for evaluating quiz answers
        correct_answers = [2, 3, 1, 2]
        score = sum(1 for i, answer in enumerate(answers) if answer == correct_answers[i])
        return score >= 3

    def submit_adoption_request(self, username, pet_id, quiz_result):
        if quiz_result:
            # Update pet status
            for pet in self.pets:
                if pet["id"] == pet_id:
                    pet["status"] = "Adopted"
                    break
            # Update user status
            self.users[username] = {"status": "Adopter", "adopted_pet": pet_id}

    def check_adoption_updates(self, adopter_id):
        user = self.users.get(adopter_id)
        if user and user["status"] == "Adopter":
            return f"Adoption update: You successfully adopted pet ID {user['adopted_pet']}."
        return "No adoption updates available."
