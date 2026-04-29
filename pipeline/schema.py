from utils.llm_client import call_llm

def generate_schema(intent_json):
    
    prompt = f"""
    Based on this intent:
    {intent_json}

    Generate STRICT JSON with:
    - ui_schema (pages, components)
    - api_schema (endpoints)
    - db_schema (tables)

    Ensure valid JSON only.
    """

    return call_llm(prompt)
