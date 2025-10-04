from pydantic import BaseModel

class SheetRequest(BaseModel):
    url: str

class QuestionRequest(BaseModel):
    question: str