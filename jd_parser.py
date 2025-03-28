from mistralai.client import MistralClient
import os
from dotenv import load_dotenv

# Load environment variables from a .env file (used to securely store API keys)
load_dotenv()

def load_jd(filepath: str) -> str:
    """
    Reads a job description from a plain text file.

    Parameters:
        filepath (str): Path to the job description file.

    Returns:
        str: Full job description as text.
    """
    with open(filepath, 'r') as f:
        return f.read()


def extract_requirements(job_description: str) -> str:
    """
    Uses Mistral to extract structured requirements from a job description.

    Parameters:
        job_description (str): Raw text of the job description.

    Returns:
        str: Extracted skills, tools, experience, and a short summary.
    """
    # Construct a clear, recruiter-style prompt for the LLM
    prompt = f"""
    Given the following job description, extract:
    - Key skills
    - Required experience
    - Tools/technologies
    - Qualifications
    Then give a 2-3 line summary.

    Job Description:
    {job_description}
    """

    # Initialize Mistral client using API key from env
    client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))

    # Call the model with the structured prompt
    response = client.chat(
        model="mistral-medium",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Return the extracted and summarized output
    return response.choices[0].message.content
