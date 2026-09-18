from document_service import extract_pages_from_pdf
from chunking_service import chunk_pages
from embedding_service import create_embeddings
from vector_store import create_vector_index


def process_document(uploaded_file):
    """
    Process an uploaded PDF and create a searchable vector index
    while preserving page numbers for each chunk.
    """

    # 1. Extract text page-by-page
    pages = extract_pages_from_pdf(uploaded_file)

    # 2. Split each page into chunks
    chunks = chunk_pages(pages)

    # 3. Create embeddings using chunk text
    embeddings = create_embeddings(chunks)

    # 4. Create FAISS vector index
    index = create_vector_index(embeddings)

    return {
        "pages": pages,
        "chunks": chunks,
        "embeddings": embeddings,
        "index": index
    }