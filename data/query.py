from dotenv import load_dotenv
import os
from groq import Groq
from langchain.prompts import PromptTemplate
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb
from chromadb.config import Settings
import faiss
import numpy as np
from langchain.vectorstores import FAISS


load_dotenv()
GROQ_API = os.environ.get("GROQ_ENV")


#extracting data from the pdf
def load_pdf(data):
    loader = DirectoryLoader(data, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    return documents

def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    text_chunks = text_splitter.split_documents(extracted_data)

    return text_chunks


# download embedding model
def download_hugging_face_embeddings():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2") #sentence transformers
    return embeddings


embeddings = download_hugging_face_embeddings()


from langchain.docstore.document import Document

def store_embeddings_in_faiss_langchain(text_chunks, embeddings_model):
    # Initialize the embedding model (sentence-transformers/all-MiniLM-L6-v2)

    # Prepare the texts and corresponding embeddings
    texts = [chunk.page_content for chunk in text_chunks]  # Extract text content from chunks
    
    # Use LangChain's FAISS to generate embeddings and store them
    faiss_store = FAISS.from_texts(texts, embeddings_model)

    return faiss_store  # Returns the FAISS vector store with indexed documen


# Function to query FAISS for the nearest neighbors
def query_faiss(index, embeddings_model, query_text, texts, k=3):
    # Generate the embedding for the query using `embed_query`
    query_embedding = embeddings_model.embed_query(query_text)  # Pass string directly, not a list
    
    # Perform similarity search (find k nearest neighbors)
    distances, indices = index.search(np.array([query_embedding], dtype="float32"), k)
    
    # Retrieve the corresponding texts for the nearest neighbors
    results = [texts[i] for i in indices[0]]
    
    return results, distances



# Function to query the FAISS vector store


def query_faiss_langchain(faiss_store, query_text):

    # Initialize the embedding model again for query embedding generation
    embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Perform the similarity search on the FAISS index
    results = faiss_store.similarity_search(query_text, k=3)  # Retrieve top-k most similar documents

    return results

def generate_llama_response(client, query_text, retrieved_texts):
    # Create a prompt with the query and the retrieved documents
    template = """You are a helpful assistant. Use the following retrieved documents to answer the question in a helpful way.

    Retrieved Documents:
    {retrieved_texts}
    
    Question: {query_text}
    
    Answer:"""
    
    # Define the PromptTemplate
    prompt = PromptTemplate(
        input_variables=["retrieved_texts", "query_text"],
        template=template,
    )
    
    # Format the prompt with the retrieved documents and query
    formatted_prompt = prompt.format(
        retrieved_texts="\n".join(retrieved_texts),
        query_text=query_text,
    )
    
    # Call the Groq LLaMA3 model to generate an answer
    # chat_completion = client.chat.completions.create(
    #     messages=[
    #         {
    #             "role": "system",
    #             "content": "You are a helpful assistant."
    #         },
    #         {
    #             "role": "user",
    #             "content": formatted_prompt,  # Pass the formatted prompt as the user input
    #         }
    #     ],
    #     model="llama3-8b-8192",  # Adjust model as necessary
    #     temperature=0.5,          # Adjust the temperature for randomness
    #     top_p=0.9,                # Use top-p sampling for diversity
    #     stop=None,                # Option to define stopping tokens
    #     max_tokens=200            # Limit the number of tokens in the response
    # )

    response = client.generate(formatted_prompt)

    # Extract and return the generated answer from the response
    # return chat_completion.choices[0].message.content
    return response

query_text = "Where is Mount Everest located?"

    # Step 1: Retrieve relevant documents from FAISS
retrieved_texts = query_faiss_langchain(faiss_store, query_text)

retrieved_texts = "\n".join(retrieved_texts[0])


    # Step 2: Use LLaMA to generate an answer based on the retrieved documents
answer = generate_llama_response(client, query_text, retrieved_texts[0])

    # Print the generated answer
print("Generated Answer:", answer)