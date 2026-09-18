class QuizEngine:

    def __init__(self, quiz):
        self.quiz = quiz
        self.current_question = 0
        self.score = 0
        self.answered = False

    def get_current_question(self):
        if self.current_question >= len(self.quiz):
            return None

        return self.quiz[self.current_question]

    def submit_answer(self, selected_answer):
        question = self.get_current_question()

        if question is None:
            return None

        self.answered = True

        correct_answer = question["correct_answer"]

        is_correct = (
            selected_answer == correct_answer
        )

        if is_correct:
            self.score += 1

        return {
            "is_correct": is_correct,
            "correct_answer": correct_answer,
            "explanation": question["explanation"],
            "page_number": question["page_number"]
        }

    def next_question(self):

        if self.current_question < len(self.quiz) - 1:

            self.current_question += 1
            self.answered = False

            return True

        return False

    def is_complete(self):
        return (
            self.current_question >= len(self.quiz) - 1
            and self.answered
        )

    def get_score(self):
        return self.score

    def get_total_questions(self):
        return len(self.quiz)

    def get_percentage(self):

        if len(self.quiz) == 0:
            return 0

        return (
            self.score / len(self.quiz)
        ) * 100