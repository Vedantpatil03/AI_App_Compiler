from pydantic import BaseModel
from typing import Dict

class AppSchema(BaseModel):
    ui_schema: Dict
    api_schema: Dict
    db_schema: Dict
    # new auth schema for authentication/authorization output
    auth_schema: Dict