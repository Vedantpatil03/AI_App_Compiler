from utils.llm_client import call_llm

def extract_intent(user_prompt):
    prompt = f"""
    Extract structured intent from this user request.

    Input:
    {user_prompt}

    Output JSON with:
    - features (list)
    - roles (list)
    - description
    """

    return call_llm(prompt)