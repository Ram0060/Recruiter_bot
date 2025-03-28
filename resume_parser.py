def extract_resume_text(filepath: str) -> str:
    """
    Reads the candidate's resume from a plain text (.txt) file.
    
    Parameters:
        filepath (str): Path to the resume text file.

    Returns:
        str: Entire resume as plain text.
    """
    # Open the file using UTF-8 encoding to handle special characters in resumes
    with open(filepath, "r", encoding="utf-8") as f:
        # Read the entire content and strip leading/trailing whitespace
        return f.read().strip()
