from document_service import extract_text_from_pdf
from chunking_service import chunk_text
from embedding_service import create_embeddings
from vector_store import create_vector_index, search_similar_chunks


# 1. Read PDF
with open("sample.pdf", "rb") as pdf_file:
    text = extract_text_from_pdf(pdf_file)


# 2. Create chunks
chunks = chunk_text(text)


# 3. Create embeddings
embeddings = create_embeddings(chunks)


# 4. Create vector index
index = create_vector_index(embeddings)


# 5. Ask a question
question = "What do I need to learn to become a data scientist?"


# 6. Create embedding for the question
query_embedding = create_embeddings([question])[0]


# 7. Search for relevant chunks
distances, indices = search_similar_chunks(
    index,
    query_embedding,
    top_k=3
)


# 8. Display results
print("\nQUESTION:")
print(question)

print("\nMOST RELEVANT CHUNKS:")
print("=" * 60)

for rank, (distance, index_number) in enumerate(
    zip(distances, indices),
    start=1
):
    print(f"\nRESULT {rank}")
    print(f"Distance: {distance}")
    print(f"Chunk number: {index_number}")
    print("-" * 60)
    print(chunks[index_number][:1000])