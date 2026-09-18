from document_service import extract_text_from_pdf

with open("sample.pdf", "rb") as pdf_file:
    text = extract_text_from_pdf(pdf_file)

print("PDF TEXT EXTRACTED SUCCESSFULLY!")
print("----------------------------------")
print(text[:3000])