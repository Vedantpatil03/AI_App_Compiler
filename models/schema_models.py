from pydantic import BaseModel
from typing import Dict

class AppSchema(BaseModel):
    ui_schema: Dict
    api_schema: Dict
    db_schema: Dict