from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
import os
import sqlite3
import re

# --- Configuration ---
GOOGLE_API_KEY = "AIzaSyA8EZwS-2jKBvSulHMnl43ZQGHlorhntiQ"  # Replace with your key
db_path = "cricket_analysis.db"

# --- Langchain Setup ---
def create_db_chain(db_uri, llm):
    """Creates and returns the Langchain SQLDatabaseChain."""
    input_db = SQLDatabase.from_uri(db_uri)
    db_chain = SQLDatabaseChain.from_llm(llm=llm, db=input_db, verbose=False, return_intermediate_steps=False)
    return db_chain

# --- Main Execution ---
if __name__ == "__main__":
    print("Welcome to the Cricket Query Assistant (Langchain + Gemini)\n")
    print("Ask cricket-related questions")

    if not os.path.exists(db_path):
        print(f"Database not found at: {db_path}")
        exit()

    db_uri = f"sqlite:///{db_path}"
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)
    db_agent = create_db_chain(db_uri, llm)

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break
        try:
            # Get response from the LLM
            response = db_agent.invoke({"query": user_input})
            response_text = response.strip() if isinstance(response, str) else str(response)

            # Extracting and formatting the clean answer
            # Check if 'result' is present in the response
            if 'result' in response:
                result = response['result']
                print(f"Assistant: {result}")  # Direct, clean answer

            # If no direct result found, print a fallback message
            else:
                print("Assistant: I couldn't find the answer to your query.")

        except Exception as e:
            print(f"❌ An error occurred: {e}")
