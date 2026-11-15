import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

def main():
    # LangChain automatically looks for the OPENAI_API_KEY environment variable,
    # so we do not need to hard-code it or explicitly pass it if it's set.
    load_dotenv()
    # Initialize the ChatOpenAI model
    llm = ChatOpenAI(model="gpt-4o-mini")

    # Define the strict prompt
    prompt = (
        "Give me exactly 5 healthy breakfast ideas. "
        "Format the output strictly as a numbered list, one line each, with no preamble and no closing text."
    )

    # Ask the model
    response = llm.invoke(prompt)

    # Print only the text content of the reply, not the full AIMessage object
    print(response.content)

if __name__ == "__main__":
    main()