from pydantic import BaseModel

class TryEntry(BaseModel):
    user_id: int
    recipe_id: int