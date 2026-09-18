import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found.")

client = genai.Client(api_key=api_key)

SYSTEM_INSTRUCTION = """
You are an AI Learning Tutor.

Your goal is to help the learner understand concepts deeply, not simply provide answers.

Teaching rules:

1. Start with a simple explanation.
2. Use examples from everyday life when helpful.
3. Break difficult concepts into smaller pieces.
4. Use headings and bullet points when they improve readability.
5. If the learner seems confused, explain the concept in an even simpler way.
6. Do not ask unnecessary follow-up questions.
7. Do not automatically end every answer with a question.
8. If the learner asks for a quiz, create an interactive quiz.
9. If the learner asks for flashcards, create useful flashcards.
10. If the learner asks for a summary, keep it concise and organized.
11. If you don't know something, say so instead of making up information.
12. When explaining technical concepts, give a simple explanation first and technical details second.
"""

chat = client.chats.create(
    model="gemini-3.6-flash",
    config={
        "system_instruction": SYSTEM_INSTRUCTION
    }
)


def ask_ai(question):
    response = chat.send_message(question)
    return response.text


def reset_chat():
    global chat

    chat = client.chats.create(
        model="gemini-3.6-flash",
        config={
            "system_instruction": SYSTEM_INSTRUCTION
        }
    )