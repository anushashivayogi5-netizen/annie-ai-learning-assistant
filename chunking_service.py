def chunk_pages(pages, chunk_size=1000, overlap=200):
    chunks = []

    for page in pages:

        page_number = page["page_number"]
        text = page["text"]

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk = text[start:end].strip()

            if chunk:
                chunks.append({
                    "text": chunk,
                    "page_number": page_number
                })

            start += chunk_size - overlap

    return chunks