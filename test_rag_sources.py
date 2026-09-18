from document_manager import process_document
from rag_service import generate_rag_answer


# Load and process PDF
with open("sample.pdf", "rb") as pdf_file:
    document = process_document(pdf_file)


# Ask a question
question = "What do I need to learn to become a data scientist?"


# Run RAG
answer, sources = generate_rag_answer(
    question,
    document["chunks"],
    document["index"],
    top_k=3
)


print("\nQUESTION:")
print(question)

print("\nRAG ANSWER:")
print("=" * 60)
print(answer)

print("\nSOURCES:")
print("=" * 60)

for source in sources:

    print(
        f"Page {source['page_number']} "
        f"| Distance: {source['distance']:.4f} "
        f"| Chunk: {source['chunk_index']}"
    )