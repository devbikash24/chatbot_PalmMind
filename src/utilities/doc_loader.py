from .create_vectordb import PrepareFAISSVectorDB
from typing import List, Tuple
import os
import logging


class UploadFile:
    """
    Utility class for handling file uploads and processing.

    This class provides static methods for checking directories and processing uploaded files
    to prepare a FAISS VectorDB or summarize the content.
    """

    @staticmethod
    def save_uploaded_files(uploaded_files: List, save_dir: str) -> List[str]:
        """
        Save the uploaded files to a directory.

        Parameters:
            uploaded_files (List): List of uploaded files (could be multiple files).
            save_dir (str): The directory where the files will be saved.

        Returns:
            List[str]: A list of file paths of the saved files.
        """
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        saved_file_paths = []
        for file in uploaded_files:
            file_path = os.path.join(save_dir, file.filename)
            with open(file_path, "wb") as f:
                f.write(file.read())  # Save file content
            saved_file_paths.append(file_path)

        return saved_file_paths

    @staticmethod
    def process_uploaded_files(files_dir: List, chatbot: List, action: str, app_config) -> Tuple[str, List]:
        """
        Process uploaded files to either prepare a FAISS VectorDB or provide a summary.

        Parameters:
            files_dir (List): List of paths to the uploaded files.
            chatbot: An instance of the chatbot for communication.
            action (str): The action to take, either 'Process for RAG' or 'Give Full Summary'.
            app_config: Configuration object with settings for processing files (embedding model, chunk size, etc.)

        Returns:
            Tuple: A tuple containing an empty string and the updated chatbot instance.
        """
            # Initialize the FAISS VectorDB creator and process files for vector storage
        prepare_vectordb_instance = PrepareFAISSVectorDB(app_config)
        prepare_vectordb_instance.prepare_and_save_vectordb()
        logging.info("Uploaded files are processed and the VectorDB is ready. Please ask your question.")

        # chatbot.append((" ", "Uploaded files are processed and the VectorDB is ready. Please ask your question."))

        return "", chatbot


# if __name__ == "__main__":
#     from load_configuration import LoadConfiguration
#     app_config = LoadConfiguration()