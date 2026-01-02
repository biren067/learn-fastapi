
from pydantic import BaseModel

from typing import Optional

class Book(BaseModel):
	id: int
	title: str
	author: str

class CreateBook(BaseModel):
	title: str
	author: str

class UpdateBook(BaseModel):
    title: str      # Required
    author: str     # Required
    
class PartialBook(BaseModel):
    title: Optional[str] = None    # Optional
    author: Optional[str] = None   # Optional