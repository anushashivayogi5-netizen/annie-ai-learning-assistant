from document_service import extract_text_from_pdf
from chunking_service import chunk_text
from embedding_service import create_embeddings
from vector_store import create_vector_index
from rag_service import generate_rag_answer


# -----------------------------
# 1. Load PDF
# -----------------------------

with open("sample.pdf", "rb") as pdf_file:
    text = extract_text_from_pdf(pdf_file)


# -----------------------------
# 2. Create chunks
# -----------------------------

chunks = chunk_text(text)


# -----------------------------
# 3. Create embeddings
# -----------------------------

embeddings = create_embeddings(chunks)


# -----------------------------
# 4. Create vector index
# -----------------------------

index = create_vector_index(embeddings)


# -----------------------------
# 5. Ask question
# -----------------------------

question = "What do I need to learn to become a data scientist?"


# -----------------------------
# 6. RAG
# -----------------------------

answer, relevant_chunks = generate_rag_answer(
    question,
    chunks,
    index,
    top_k=3
)


# -----------------------------
# 7. Display answer
# -----------------------------

print("\nQUESTION:")
print(question)

print("\nRAG ANSWER:")
print("=" * 60)
print(answer)

print("\nRETRIEVED CHUNKS:")
print("=" * 60)

for i, chunk in enumerate(relevant_chunks, start=1):

    print(f"\nChunk {i}")
    print(f"Distance: {chunk['distance']}")
    print(f"Chunk index: {chunk['chunk_index']}")
    print("-" * 60)
    print(chunk["text"][:500])