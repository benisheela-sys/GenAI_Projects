# Qwen Chat Bot with Ollama

A simple Python chatbot that uses the local Ollama model `qwen2.5:0.5b`.

## Prerequisites

- Python 3.10+
- Ollama installed
- Qwen model downloaded

Download the model:

```bash
ollama pull qwen2.5:0.5b
```

Install the Python package:

```bash
pip install ollama
```

## Python Code

```python
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
```

## Run the Application

```bash
python ollama_sample.py
```

## Example

```text
Qwen Chat Bot (type 'exit' to quit)

You: write a email to apply a job position for biztalk developer

Bot: Dear Hiring Manager,
I am writing to apply for the position of BizTalk Developer at [Company Name]. I am a [name] with [years of experience] of experience in [related field]. I am passionate about [reason for applying]. I have a strong background in [relevant skills or knowledge].
I am excited about the opportunity to join [Company Name] and contribute to the success of the team. I have a good understanding of [related field] and have been successful in [relevant experience].
I am looking forward to hearing from you and I look forward to the opportunity to discuss how I can contribute to [Company Name].
Thank you for considering my application. I look forward to hearing from you soon.
Sincerely,
[Your Name]

You: exit
```

## Features

- Runs completely locally
- No API key required
- Uses Ollama and Qwen 2.5
- Interactive command-line chat experience