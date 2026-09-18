from document_service import extract_text_from_pdf
from chunking_service import chunk_text
from embedding_service import create_embeddings


# Extract text from PDF
with open("sample.pdf", "rb") as pdf_file:
    text = extract_text_from_pdf(pdf_file)


# Create chunks
chunks = chunk_text(text)


# Create embeddings
embeddings = create_embeddings(chunks)


print("Number of chunks:", len(chunks))
print("Number of embeddings:", len(embeddings))
print("Embedding size:", len(embeddings[0]))

print("\nFirst embedding:")
print(embeddings[0])