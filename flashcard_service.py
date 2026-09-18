import json

from gemini_service import client


def generate_flashcards(
    context,
    num_cards=5,
    difficulty="Beginner"
):

    prompt = f"""
You are an AI Learning Tutor creating flashcards for a student.

Create {num_cards} flashcards using ONLY the document context below.

Difficulty: {difficulty}

IMPORTANT:
- Flashcards must be based on the provided document.
- Do not invent information.
- Keep the front concise.
- The back should clearly explain the concept.
- Include the source page number.
- Return ONLY valid JSON.
- Do not include markdown or ```json.

Return exactly this structure:

[
    {{
        "front": "Question or concept",
        "back": "Clear explanation or answer",
        "page_number": 12
    }}
]

DOCUMENT CONTEXT:
-------------------------
{context}
-------------------------
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    response_text = response.text.strip()

    # Remove markdown fences if Gemini adds them
    if response_text.startswith("```"):
        response_text = (
            response_text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

    flashcards = json.loads(response_text)

    return flashcards