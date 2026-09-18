from document_service import extract_text_from_pdf
from chunking_service import chunk_text

with open("sample.pdf", "rb") as pdf_file:
    text = extract_text_from_pdf(pdf_file)

chunks = chunk_text(text)

print("Total characters:", len(text))
print("Total chunks:", len(chunks))

print("\n--- FIRST CHUNK ---")
print(chunks[0])

print("\n--- SECOND CHUNK ---")
print(chunks[1])