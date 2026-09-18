from gemini_service import ask_ai

print("🤖 AI Learning Chatbot")
print("Type 'exit' to quit.\n")

while True:
    user_message = input("You: ")

    if user_message.lower() == "exit":
        print("Goodbye! 👋")
        break

    if not user_message.strip():
        print("Please enter a question.")
        continue

    try:
        answer = ask_ai(user_message)
        print("AI:", answer)
        print()

    except Exception as e:
        print("Sorry, something went wrong:", e)