class AdoptionQuizService:
    def __init__(self):
        self.questions = [
            "How much time can you dedicate to taking care of a pet daily?",
            "How familiar are you with pet health and care?",
            "Are you willing to adopt a pet from a shelter?",
            "Do you have experience with training pets?",
            "Do you have a pet care emergency plan?",
        ]
        self.options = [
            ["1-2 hours", "3-4 hours", "5+ hours", "None"],
            ["None", "Some experience", "Moderate experience", "Expert"],
            ["Yes", "No", "Not sure", "Already adopted from a shelter"],
            ["None", "Basic training", "Advanced training", "Expert trainer"],
            ["No", "Yes, I have a plan", "I am considering one", "Not sure"],
        ]
        self.correct_answers = [2, 2, 0, 2, 1]  # Expected correct indices

    def ask_adoption_quiz(self, username, answers):
        score = 0
        result=False
        for i, answer in enumerate(answers):
            if answer - 1 == self.correct_answers[i]:
                score += 1
                if score >= 3:
                    result=True
        return result

    # def choose_adoption(self, username):
    #     # Assume the user opts to take the quiz
    #     # This could involve other business logic if required.
    #     return True
