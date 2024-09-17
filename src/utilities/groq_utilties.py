from langchain.prompts import PromptTemplate

from src.utilities.load_configuration import LoadConfiguration

app_config = LoadConfiguration()

def generate_groq_response(client, query_text: str, retrieved_texts: list) -> str:
    """
    Generates a response using Groq API based on the provided query and retrieved documents.

    Args:
        client: The Groq API client for generating completions.
        query_text (str): The user's query.
        retrieved_texts (list): A list of texts retrieved from the document search.

    Returns:
        str: The generated response from Groq API or an error message if an exception occurs.
    """
    # Create a prompt template
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
    
    try:
        # Create a response using the Groq client
        response = client.chat.completions.create(  # Adjust based on Groq API
            messages=[
                {"role": "system", "content": formatted_prompt}
            ],
            model= app_config.llm_model, # Adjust to the Groq model being used
            temperature= app_config.temperature,  # Set temperature for response creativity
            max_tokens= app_config.max_tokens  # Limit the number of tokens in the response
        )

        # Return the generated answer from the response
        return response.choices[0].message.content
    
    except Exception as e:
        # Return an error message in case of failure
        return f"Error in generating response: {str(e)}"
