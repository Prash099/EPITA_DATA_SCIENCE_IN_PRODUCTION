from pydantic import BaseModel

class UserInput(BaseModel):
    x: int
    y: int