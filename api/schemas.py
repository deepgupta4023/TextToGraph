from pydantic import BaseModel
from typing import Optional

class TextRequest(BaseModel):
    text: str


class QueryRequest(BaseModel):
    question: str
    llm_backend:Optional[str] 
