from quiz_engine import QuizEngine


# Simple test quiz
quiz = [
    {
        "question": "What is Python?",
        "options": [
            "Programming language",
            "Database",
            "Operating system",
            "Browser"
        ],
        "correct_answer": "Programming language",
        "explanation": "Python is a programming language.",
        "page_number": 1
    },
    {
        "question": "What is AI?",
        "options": [
            "Artificial Intelligence",
            "Apple Internet",
            "Automated Internet",
            "None"
        ],
        "correct_answer": "Artificial Intelligence",
        "explanation": "AI stands for Artificial Intelligence.",
        "page_number": 2
    }
]


# Create quiz engine
engine = QuizEngine(quiz)


# Question 1
question = engine.get_current_question()

print("\nQUESTION 1")
print(question["question"])


# Submit correct answer
result = engine.submit_answer(
    "Programming language"
)

print("\nRESULT")
print(result)


# Move to Question 2
engine.next_question()

question = engine.get_current_question()

print("\nQUESTION 2")
print(question["question"])


# Submit wrong answer
result = engine.submit_answer(
    "Apple Internet"
)

print("\nRESULT")
print(result)


# Final score
print("\nFINAL SCORE")
print(
    f"{engine.get_score()} / "
    f"{engine.get_total_questions()}"
)

print(
    f"Percentage: "
    f"{engine.get_percentage()}%"
)