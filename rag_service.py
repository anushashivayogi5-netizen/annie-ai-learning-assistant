from embedding_service import create_embeddings
from vector_store import search_similar_chunks
from gemini_service import client


def retrieve_relevant_chunks(
    question,
    chunks,
    index,
    top_k=3
):
    # Create an embedding for the user's question
    query_embedding = create_embeddings([{
        "text": question,
        "page_number": 0
    }])[0]

    # Search FAISS
    distances, indices = search_similar_chunks(
        index,
        query_embedding,
        top_k
    )

    relevant_chunks = []

    for distance, index_number in zip(distances, indices):

        chunk = chunks[index_number]

        relevant_chunks.append({
            "text": chunk["text"],
            "page_number": chunk["page_number"],
            "distance": float(distance),
            "chunk_index": int(index_number)
        })

    return relevant_chunks


def generate_rag_answer(
    question,
    chunks,
    index,
    top_k=3
):
    # Retrieve relevant document chunks
    relevant_chunks = retrieve_relevant_chunks(
        question,
        chunks,
        index,
        top_k
    )

    # Combine retrieved chunks into context
    context_parts = []

    for chunk in relevant_chunks:

        context_parts.append(
            f"[Page {chunk['page_number']}]\n"
            f"{chunk['text']}"
        )

    context = "\n\n".join(context_parts)

    # Create grounded prompt
    prompt = f"""
You are an AI Learning Tutor.

Answer the user's question using the provided document context.

IMPORTANT:
- Base your answer primarily on the provided context.
- Do not invent information that is not supported by the context.
- If the context does not contain enough information to answer,
  clearly say that the document does not provide enough information.
- Explain the answer clearly for a learner.
- Use bullet points when helpful.
- When making a factual claim from the document, mention the relevant page number.

DOCUMENT CONTEXT:
-----------------
{context}
-----------------

USER QUESTION:
{question}
"""

    # Ask Gemini
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text, relevant_chunks