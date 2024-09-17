import os
import pickle
import logging
from typing import List
from pathlib import Path
from langchain.vectorstores import FAISS
from langchain_community.document_loaders import DirectoryLoader, TextLoader, UnstructuredWordDocumentLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings

class MultiFormatDocumentLoader:
    """
    A class to load documents of multiple types (PDF, Word, Text) from a directory.
    """

    def __init__(self, data_directory: str) -> None:
        self.data_directory = data_directory

    def load_documents(self) -> List:
        """
        Load documents from the directory, supporting PDF, Word (docx), and text files.

        Returns:
            List: A list of loaded documents.
        """
        # Create loaders for different file types
        pdf_loader = DirectoryLoader(self.data_directory, glob="*.pdf", loader_cls=PyPDFLoader)
        word_loader = DirectoryLoader(self.data_directory, glob="*.docx", loader_cls=UnstructuredWordDocumentLoader)
        text_loader = DirectoryLoader(self.data_directory, glob="*.txt", loader_cls=TextLoader)

        # Load all documents
        pdf_docs = pdf_loader.load()
        word_docs = word_loader.load()
        text_docs = text_loader.load()

        # Combine all loaded documents into one list
        all_docs = pdf_docs + word_docs + text_docs
        return all_docs


class PrepareFAISSVectorDB:
    """
    A class for preparing and saving a FAISS VectorDB using Hugging Face embeddings.

    This class facilitates the process of loading documents, chunking them, and creating a FAISS VectorDB.
    It provides methods to prepare and save the VectorDB.

    Parameters:
        app_config (object): Configuration object containing directories, chunk size, overlap, and embeddings.
    """

    def __init__(self, app_config) -> None:
        """
        Initialize the PrepareFAISSVectorDB instance.
        """
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=app_config.chunk_size,
            chunk_overlap=app_config.chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        self.data_directory = app_config.directories_for_doc
        self.persist_directory = app_config.persistent_directory
        self.embedding = app_config.embedding_model

    def __load_and_chunk_documents(self) -> List:
        """
        Load and chunk the documents from the directory.

        Returns:
            List: A list of chunked documents.
        """
        logging.info("Loading documents from the directory...")

        # Use MultiFormatDocumentLoader to load documents from multiple formats
        loader = MultiFormatDocumentLoader(self.data_directory)
        docs = loader.load_documents()

        logging.info(f"Loaded {len(docs)} documents. Now chunking the documents...")

        # Chunk the loaded documents
        chunked_documents = self.text_splitter.split_documents(docs)
        logging.info(f"Chunked the documents into {len(chunked_documents)} chunks.")
        return chunked_documents

    def prepare_and_save_vectordb(self) -> FAISS:
        """
        Load, chunk, and create a FAISS VectorDB with Hugging Face embeddings, and save it.

        Returns:
            FAISS: The created FAISS VectorDB.
        """
        # Load and chunk the documents
        chunked_documents = self.__load_and_chunk_documents()
        texts = [chunk.page_content for chunk in chunked_documents]
        logging.info("Preparing FAISS VectorDB...")

        # Create FAISS vector store using Hugging Face embeddings
        vectordb = FAISS.from_texts(
            texts=texts,
            embedding=HuggingFaceEmbeddings(model_name=self.embedding)
        )

        # Define paths for saving the FAISS index and metadata
        faiss_index_path = os.path.join(self.persist_directory, "faiss_index")
        metadata_path = os.path.join(self.persist_directory, "faiss_metadata.pkl")

        # Save FAISS index
        vectordb.save_local(faiss_index_path)

        # Save metadata to match the FAISS index with the original documents
        with open(metadata_path, "wb") as metadata_file:
            pickle.dump(chunked_documents, metadata_file)

        logging.info("FAISS VectorDB is created and saved.")
        logging.info(f"Number of vectors in the VectorDB: {len(chunked_documents)}")
        return vectordb

    def load_vectordb(self) -> FAISS:
        """
        Load the FAISS index and metadata from the persist directory.

        Returns:
            FAISS: The loaded FAISS VectorDB.
        """
        logging.info("Loading FAISS VectorDB...")

        faiss_index_path = os.path.join(self.persist_directory, "faiss_index")
        metadata_path = os.path.join(self.persist_directory, "faiss_metadata.pkl")

        # Load FAISS index
        vectordb = FAISS.load_local(faiss_index_path, self.embedding, allow_dangerous_deserialization=True)

        # Load metadata (original documents)
        with open(metadata_path, "rb") as metadata_file:
            chunked_documents = pickle.load(metadata_file)

        logging.info(f"Loaded FAISS VectorDB with {len(chunked_documents)} vectors.")
        return vectordb
