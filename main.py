from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
class Book(BaseModel):
	title: str
	author: str

app = FastAPI()

@app.get("/")
async def books()-> List[Book]:
	book1 = Book(title="Rich Dad Poor Dad", author="kyolink")
	book2 = Book(title="The Maurya Samaj", author="Vishnu gupta")

	books = [book1,book2]

	return books