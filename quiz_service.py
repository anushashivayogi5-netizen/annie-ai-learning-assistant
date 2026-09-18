import json

from gemini_service import client


def generate_quiz(
    context,
    num_questions=5,
    difficulty="Beginner"
):

    prompt = f"""
You are an AI Learning Tutor creating a quiz for a student.

Create a {num_questions}-question multiple-choice quiz using ONLY
the document context provided below.

Difficulty: {difficulty}

IMPORTANT:
- Questions must be based on the document.
- Each question must have exactly 4 answer choices.
- There must be exactly one correct answer.
- Do not make up information that is not supported by the document.
- Include the page number where the answer was found.
- Include a short, clear topic name for each question.
- Return ONLY valid JSON.
- Do not include markdown or code fences.

Return this exact JSON structure:

[
    {{
        "question": "Question text",
        "options": [
            "Option A",
            "Option B",
            "Option C",
            "Option D"
        ],
        "correct_answer": "Option A",
        "explanation": "Brief explanation",
        "page_number": 12,
        "topic": "Short topic name"
    }}
]

DOCUMENT CONTEXT:
-------------------------
{context}
-------------------------
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    response_text = response.text.strip()

    if response_text.startswith("```"):

        response_text = response_text.replace(
            "```json",
            ""
        ).replace(
            "```",
            ""
        ).strip()

    quiz = json.loads(response_text)

    return quiz