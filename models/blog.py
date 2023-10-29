from pydantic import BaseModel
from datetime import datetime


class Blog(BaseModel):
    title: str
    content: str
    created_at: datetime = None
