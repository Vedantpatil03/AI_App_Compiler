import json
import re
from models.schema_models import AppSchema

def extract_json(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    return match.group(0) if match else text

def validate_schema(schema_str):
    try:
        if isinstance(schema_str, dict):
            data = schema_str
        else:
            clean_json = extract_json(schema_str)
            data = json.loads(clean_json)

        validated = AppSchema(**data)
        return validated.model_dump(), None
    except Exception as e:
        return None, str(e)