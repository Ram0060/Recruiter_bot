from mistralai.client import MistralClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file (e.g., API key)
load_dotenv()

# Initialize Mistral client using the API key from env
client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))

def summarize_answer(question: str, answer: str, model="mistral-medium") -> str:
    """
    Generates a neutral, factual summary of the candidate's response using Mistral.

    Parameters:
        question (str): The interview question asked.
        answer (str): The candidate's full response.
        model (str): Mistral model to use (default: mistral-medium)

    Returns:
        str: A 4–6 sentence summary of the response.
    """

    # Create a clear instruction prompt for the LLM
    prompt = f"""
As a recruiter, summarize the candidate's response to the following interview question.

Question: {question}

Answer: {answer}

Summarize it in 4-6 sentences, highlighting the key points mentioned. Be neutral and factual.
    """

    # Call the Mistral chat model with the user prompt
    response = client.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    # Extract the generated summary text from the response object
    return response.choices[0].message.content.strip()
