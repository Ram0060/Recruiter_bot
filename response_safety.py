# Checks if the candidate's response expresses uncertainty
def is_uncertain_response(text: str) -> bool:
    text = text.lower().strip()
    # Look for common phrases that indicate the candidate isn't confident or doesn't know the answer
    return any(phrase in text for phrase in [
        "i don't know",
        "not sure",
        "no idea",
        "i have no idea",
        "i'm not sure"
    ])

# Checks if the response is too short to be meaningful
def is_too_short(text: str, min_words=5) -> bool:
    # Minimum word count helps filter out weak answers like "yes", "maybe", "I guess", etc.
    return len(text.strip().split()) < min_words

# Checks if the response is basically empty (e.g., silence, whitespace)
def is_empty(text: str) -> bool:
    # Strip spaces and check if there's anything left
    return not text.strip()
