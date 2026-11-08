import ollama

print("Qwen Chat Bot (type 'exit' to quit)")

while True:
    user_input = input("\nYou: ")

    if user_input.lower() == "exit":
        break

    response = ollama.chat(
        model="qwen2.5:0.5b",
        messages=[
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    print("\nBot:", response["message"]["content"])