"""
Script to vectorize directory and generate responses from a ChatOpenAI model.

Usage in command line: 
python embed.py your_directory

Arguments:
    your_directory: Directory to embed
"""

import argparse
import os
import sys
from dotenv import load_dotenv

from langchain.document_loaders import TextLoader, DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI


def main():

    # get api key from .env file
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')

    # If the API key is None (not set), let the user know and quit, or ask for it
    if api_key is None:
        print("Please set your OPENAI_API_KEY in the .env file")
        sys.exit(1)

    # Set directory as optional command line argument
    parser = argparse.ArgumentParser(description="Generate chatbot responses")
    parser.add_argument("directory", type=str, nargs='?', default=None, help="Directory to embed, just the name if it's in the same folder as this script, include the path if it's not")
    args = parser.parse_args()
    # ask for directory if none was provided
    if args.directory is None:
        folder = input("Enter the directory to be analyzed: ")
    else:
        folder = args.directory

    # vectorize directory
    loader = DirectoryLoader(folder)

    # create index for data
    index = VectorstoreIndexCreator().from_loaders([loader])

    # create chatbot
    chat_model = ChatOpenAI(temperature=0.3)
    
    while True:
        message = input("Your message to the chatbot (type 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        else:
            print(index.query(message, llm=chat_model))

if __name__ == "__main__":
    main()
