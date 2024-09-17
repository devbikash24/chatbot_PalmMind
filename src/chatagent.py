import os
import time
import re
import ast
import html
from .utilities.load_configuration import LoadConfiguration
from .utilities.create_vectordb import PrepareFAISSVectorDB
from langchain.vectorstores import FAISS
from typing import List, Tuple
import logging
from utilities.doc_loader import UploadFile
APPCFG = LoadConfiguration()


class ChatBot:
    """
    Class representing a chatbot with document retrieval and response generation capabilities.
    Users can upload files, process them, query for responses, and clear document references.
    """

    vectordb = None  # Class attribute to hold the FAISS vector database

    @staticmethod
    def upload_and_process_files(uploaded_files: List, chatbot: List) -> Tuple:
        """
        Handle file uploads and process them to prepare a FAISS VectorDB.

        Parameters:
            uploaded_files (List): List of uploaded files.
            chatbot (List): List representing the chatbot's conversation history.
            action (str): The action to take, either 'Process for RAG' or 'Give Full Summary'.

        Returns:
            Tuple: A tuple containing an empty string and the updated chatbot instance.
        """
        if not uploaded_files:
            logging.info((" ", "Please upload some files to process."))
            # chatbot.append((" ", "Please upload some files to process."))
            # return "", chatbot

        # Save the uploaded files locally
        saved_files = UploadFile.save_uploaded_files(uploaded_files, APPCFG.upload_directory)

       
        # Prepare FAISS vector database
        prepare_vectordb_instance = PrepareFAISSVectorDB(
            APPCFG
        )
        prepare_vectordb_instance.prepare_and_save_vectordb()

        ChatBot.vectordb = prepare_vectordb_instance.load_vectordb()
        logging.info((" ", "Uploaded files are processed and the VectorDB is ready. Please ask your question."))

        # chatbot.append((" ", "Uploaded files are processed and the VectorDB is ready. Please ask your question."))

        # return "", chatbot

    @staticmethod
    def query_vector_db(message: str, chatbot: List, temperature: float = 0.0) -> Tuple:
        """
        Query the FAISS VectorDB for the user question and generate a response.

        Parameters:
            message (str): The user's query.
            chatbot (List): List representing the chatbot's conversation history.
            temperature (float): Temperature parameter for language model completion.

        Returns:
            Tuple: A tuple containing an empty string, updated chat history, and references from retrieved documents.
        """
        if ChatBot.vectordb is None:
            logging.info((" ", "VectorDB is not ready. Please upload and process files first."))
            # chatbot.append((" ", "VectorDB is not ready. Please upload and process files first."))
            # return "", chatbot, None

        # Perform similarity search in the FAISS vector database
        docs = ChatBot.vectordb.similarity_search(message, k=APPCFG.k)

        # Generate response using the OpenAI completion engine (you can customize the prompt)
        question = "# User new question:\n" + message
        retrieved_content = ChatBot.clean_references(docs)

        chat_history = f"Chat history:\n {str(chatbot[-APPCFG.number_of_q_a_pairs:])}\n\n"
        prompt = f"{chat_history}{retrieved_content}{question}"

        response = openai.ChatCompletion.create(
            messages=[
                {"role": "system", "content": APPCFG.llm_system_role},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
        )

        chatbot.append((message, response["choices"][0]["message"]["content"]))
        time.sleep(2)

        return "", chatbot, retrieved_content

    @staticmethod
    def clean_references(documents: List) -> str:
        """
        Clean and format references from retrieved documents.

        Parameters:
            documents (List): List of retrieved documents.

        Returns:
            str: A string containing cleaned and formatted references.
        """
        documents = [str(x) + "\n\n" for x in documents]
        markdown_documents = ""
        counter = 1
        for doc in documents:
            content, metadata = re.match(
                r"page_content=(.*?)( metadata=\{.*\})", doc).groups()
            metadata = metadata.split('=', 1)[1]
            metadata_dict = ast.literal_eval(metadata)

            # Clean the content
            content = html.unescape(bytes(content, "utf-8").decode("unicode_escape"))
            content = re.sub(r'\s+', ' ', content).strip()

            markdown_documents += f"# Retrieved content {counter}:\n" + content + "\n\n" + \
                                  f"Source: {os.path.basename(metadata_dict['source'])} | " + \
                                  f"Page number: {str(metadata_dict['page'])}\n\n"
            counter += 1

        return markdown_documents

    @staticmethod
    def clear_vector_db(chatbot: List) -> Tuple:
        """
        Clear the current VectorDB to allow for new document uploads.

        Parameters:
            chatbot (List): List representing the chatbot's conversation history.

        Returns:
            Tuple: An empty string and updated chat history.
        """
        ChatBot.vectordb = None
        chatbot.append((" ", "VectorDB has been cleared. You can now upload new documents."))
        return "", chatbot
