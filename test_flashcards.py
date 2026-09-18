from document_manager import process_document
from rag_service import retrieve_relevant_chunks
from flashcard_service import generate_flashcards


# --------------------------------------------
# Load PDF
# --------------------------------------------

with open("sample.pdf", "rb") as pdf_file:

    document = process_document(
        pdf_file
    )


# --------------------------------------------
# Retrieve relevant document content
# --------------------------------------------

relevant_chunks = retrieve_relevant_chunks(
    "What are the most important concepts a student should learn from this document?",
    document["chunks"],
    document["index"],
    top_k=8
)


# --------------------------------------------
# Build context
# --------------------------------------------

context_parts = []

for chunk in relevant_chunks:

    context_parts.append(
        f"[Page {chunk['page_number']}]\n"
        f"{chunk['text']}"
    )


context = "\n\n".join(
    context_parts
)


# --------------------------------------------
# Generate flashcards
# --------------------------------------------

flashcards = generate_flashcards(
    context,
    num_cards=5,
    difficulty="Beginner"
)


# --------------------------------------------
# Display flashcards
# --------------------------------------------

print("\n🃏 GENERATED FLASHCARDS")
print("=" * 60)

for number, card in enumerate(
    flashcards,
    start=1
):

    print(f"\nFLASHCARD {number}")

    print("\nFRONT:")
    print(card["front"])

    print("\nBACK:")
    print(card["back"])

    print(
        f"\nSOURCE: Page "
        f"{card['page_number']}"
    )