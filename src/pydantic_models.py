from langchain_core.pydantic_v1 import BaseModel
from typing import List

class Claim(BaseModel):
    claim: str
    sources: List[str]

class Claims(BaseModel):
    claims: List[Claim]

class Evaluation(BaseModel):
    evaluation: str
    conflict: bool

class Summary(BaseModel):
    summary: str
    needs_revision: bool