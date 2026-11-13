import os

# 1. SCRUB THE ENVIRONMENT BEFORE ANY LANGCHAIN IMPORTS
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ.pop("LANGCHAIN_API_KEY", None)
os.environ.pop("LANGCHAIN_ENDPOINT", None)
os.environ.pop("LANGCHAIN_PROJECT", None)

# 2. Now import load_dotenv and LangChain
from dotenv import load_dotenv
load_dotenv(override=True)

from langchain_openai import ChatOpenAI

# Initialize the ChatOpenAI model
llm = ChatOpenAI(model="gpt-4o-mini")

prompts = [
    "Explain the Document loader in two sentences.",
    "Explain the Text loader in two sentences.",
    "Explain the vector store in two sentences."
]

for i, prompt in enumerate(prompts, start=1):
    print(f"--- Prompt {i} ---")
    response = llm.invoke(prompt)
    print(response.content)   
    print("\n")