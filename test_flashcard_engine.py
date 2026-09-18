from flashcard_engine import FlashcardEngine


flashcards = [
    {
        "front": "What is Python?",
        "back": "Python is a programming language.",
        "page_number": 1
    },
    {
        "front": "What is AI?",
        "back": "AI stands for Artificial Intelligence.",
        "page_number": 2
    },
    {
        "front": "What is RAG?",
        "back": "RAG stands for Retrieval-Augmented Generation.",
        "page_number": 3
    }
]


# --------------------------------------------
# Create engine
# --------------------------------------------

engine = FlashcardEngine(
    flashcards
)


# --------------------------------------------
# Card 1
# --------------------------------------------

card = engine.get_current_card()

print("\nCARD 1")
print("Front:", card["front"])


# Reveal
engine.reveal_answer()

print("Back:", card["back"])


# Student knows it
engine.mark_known()


# --------------------------------------------
# Card 2
# --------------------------------------------

card = engine.get_current_card()

print("\nCARD 2")
print("Front:", card["front"])

engine.reveal_answer()

print("Back:", card["back"])


# Student needs practice
engine.mark_for_practice()


# --------------------------------------------
# Card 3
# --------------------------------------------

card = engine.get_current_card()

print("\nCARD 3")
print("Front:", card["front"])

engine.reveal_answer()

print("Back:", card["back"])


# Student knows it
engine.mark_known()


# --------------------------------------------
# Results
# --------------------------------------------

print("\nFLASHCARD RESULTS")
print("=" * 40)

print(
    "Total:",
    engine.get_total_cards()
)

print(
    "I Know This:",
    engine.get_known_count()
)

print(
    "Need Practice:",
    engine.get_practice_count()
)

print(
    "Progress:",
    f"{engine.get_progress_percentage():.0f}%"
)

print(
    "Complete:",
    engine.is_complete()
)