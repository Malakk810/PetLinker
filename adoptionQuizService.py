class AdoptionQuizService:
    def __init__(self):
        self.questions = [
            "How much time do you plan to spend with your pet?",
            "Do you have any experinace in taking care of a pet?",
            "Are you willing to adopt a pet from a shelter?",
            "Have you ever experienced pet training?",
            "If you are going somewhere and pets are not allowed, do you have an alternative plan?",
        ]
        self.options = [
            ["1-2 hours", "3-4 hours", "5+ hours", "None"],
            ["None", "Some experience", "Moderate experience", "Expert"],
            ["Yes", "No", "Not sure", "Already adopted from a shelter"],
            ["None", "Basic training", "Advanced training", "Expert trainer"],
            ["No", "Yes, I have a plan", "I am considering one", "Not sure"],
        ]
        self.correct_answers = [2, 2, 0, 2, 1]  # Expected correct indices

    def ask_adoption_quiz(self, answers):
        score = 0
        for i, answer in enumerate(answers):
            if answer - 1 == self.correct_answers[i]:
                score += 1
                if score >= 3:
                    return True
        return False
