from mistralai.client import MistralClient
import os
from dotenv import load_dotenv
import json

# Load environment variables (e.g., MISTRAL_API_KEY)
load_dotenv()

# Initialize Mistral client with API key
client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))

def process_response(question: str, answer: str, model="mistral-medium") -> tuple:
    """
    Processes the candidate's answer to a question using the Mistral LLM.

    Returns:
        tuple:
            - agent_reply (str): A comment or a follow-up question for the candidate
            - is_follow_up (bool): True if a follow-up is needed, else False
            - score (int): Numerical score (0–10) evaluating the response
    """
    # Prompt with detailed instructions and a strict JSON schema
    prompt = f"""
You are a recruiter interviewing a candidate.

Question: {question}

Candidate's Answer: {answer}

Evaluate this answer in terms of relevance, depth, clarity, and experience.
Return your response in valid JSON format with:
- score (integer out of 10)
- comment (brief feedback)
- follow_up (a follow-up question or empty string)

Example format:
{{
  "score": 8,
  "comment": "Good understanding of APIs, but needs deeper clarity on deployment.",
  "follow_up": "Can you tell me more about your experience deploying services to the cloud?"
}}
    """

    # Send prompt to the LLM
    response = client.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        # Try parsing the response content as JSON
        result = json.loads(response.choices[0].message.content)

        # Extract fields from the result with fallbacks
        score = result.get("score", 0)
        comment = result.get("comment", "")
        follow_up = result.get("follow_up", "")

        # Return follow-up if it's present, otherwise just feedback
        if follow_up:
            return follow_up, True, score  # Follow-up required
        else:
            return comment, False, score   # No follow-up needed

    except Exception as e:
        # Catch parsing errors or unexpected format
        print("⚠️ Failed to parse LLM response. Returning fallback values.")
        return "Sorry, I had trouble evaluating that answer.", False, 0
