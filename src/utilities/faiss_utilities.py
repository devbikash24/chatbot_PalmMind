import os
import pickle
import faiss
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from src.utilities.load_configuration import LoadConfiguration

# Load configuration
app_config = LoadConfiguration()

def load_faiss_index():
    """
    Loads a FAISS index and associated metadata (docstore and index_to_docstore_id) from disk.

    Returns:
        FAISS: The loaded FAISS vector store if files exist, otherwise None.
    """
    # Define paths to the FAISS index and metadata
    index_file = os.path.join(app_config.faiss_folder_for_index, "index.faiss")
    pkl_file = os.path.join(app_config.faiss_folder_for_index, "index.pkl")

    # Check if both the FAISS index and the pickle file exist
    if not os.path.exists(index_file) or not os.path.exists(pkl_file):
        return None

    try:
        # Load the FAISS index from the file
        index = faiss.read_index(index_file)
        
        # Load the document store and index-to-docstore mapping
        with open(pkl_file, 'rb') as f:
            docstore, index_to_docstore_id = pickle.load(f)

        # Return the FAISS vector store
        return FAISS(
            embedding_function=HuggingFaceEmbeddings(model_name=app_config.embedding_model),
            index=index,
            docstore=docstore,
            index_to_docstore_id=index_to_docstore_id
        )
    
    except (faiss.FaissError, pickle.UnpicklingError, IOError) as e:
        # Log the error for debugging purposes
        print(f"Error loading FAISS index or metadata: {str(e)}")
        return None
