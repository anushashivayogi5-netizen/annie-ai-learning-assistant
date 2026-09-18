from document_manager import process_document
from rag_service import retrieve_relevant_chunks
from quiz_service import generate_quiz


# --------------------------------------------
# Load PDF
# --------------------------------------------

with open("sample.pdf", "rb") as pdf_file:

    document = process_document(pdf_file)


# --------------------------------------------
# Create a learning topic/question
# --------------------------------------------

question = "What are the important skills needed to become a data scientist?"


# --------------------------------------------
# Retrieve relevant document content
# --------------------------------------------

relevant_chunks = retrieve_relevant_chunks(
    question,
    document["chunks"],
    document["index"],
    top_k=5
)


# --------------------------------------------
# Build context for quiz generation
# --------------------------------------------

context_parts = []

for chunk in relevant_chunks:

    context_parts.append(
        f"[Page {chunk['page_number']}]\n"
        f"{chunk['text']}"
    )


context = "\n\n".join(context_parts)


# --------------------------------------------
# Generate quiz
# --------------------------------------------

quiz = generate_quiz(
    context,
    num_questions=5,
    difficulty="Beginner"
)


# --------------------------------------------
# Display quiz
# --------------------------------------------

print("\n📝 GENERATED QUIZ")
print("=" * 60)

for number, question_data in enumerate(
    quiz,
    start=1
):

    print(f"\nQuestion {number}")
    print(question_data["question"])

    for index, option in enumerate(
        question_data["options"]
    ):

        print(
            f"{chr(65 + index)}. {option}"
        )

    print(
        f"\nCorrect Answer: "
        f"{question_data['correct_answer']}"
    )

    print(
        f"Explanation: "
        f"{question_data['explanation']}"
    )

    print(
        f"Source: Page "
        f"{question_data['page_number']}"
    )