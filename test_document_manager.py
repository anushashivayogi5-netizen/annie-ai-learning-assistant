from document_manager import process_document


with open("sample.pdf", "rb") as pdf_file:

    document = process_document(pdf_file)


print("DOCUMENT PROCESSED SUCCESSFULLY!")
print("--------------------------------")

print("Number of pages:", len(document["pages"]))
print("Number of chunks:", len(document["chunks"]))
print("Number of embeddings:", len(document["embeddings"]))
print("FAISS index size:", document["index"].ntotal)

print("\nFIRST CHUNK:")
print("--------------------------------")
print(document["chunks"][0]["text"][:500])

print("\nPAGE NUMBER:")
print("--------------------------------")
print(document["chunks"][0]["page_number"])