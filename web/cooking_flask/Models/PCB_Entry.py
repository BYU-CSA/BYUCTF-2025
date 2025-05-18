from pydantic import BaseModel

class PCBEntry(BaseModel):
    user_id: int
    recipe_id: int