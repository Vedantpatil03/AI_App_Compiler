from utils.llm_client import call_llm

def repair_schema(bad_schema, error):
    prompt = f"""
    Fix this JSON:
    {bad_schema}

    Error:
    {error}

    Return ONLY corrected JSON.
    """

    return call_llm(prompt)