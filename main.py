from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
import json
from typing import List,Dict,Optional
class Book(BaseModel):
	id: int
	title: str
	author: str

app = FastAPI()


def read_json()->List[Dict[str,str]]:
	contents = []
	try:
		with open("./json_data.json","r") as f:
			contents = json.load(f)
			print("Found data...",type(contents))
			return contents
	except FileNotFoundError:
		print("File not found.")
		return []
	except json.JSONDecodeError:
		print("Error: Invalid JSON format")
		return []
	

@app.get("/",status_code=status.HTTP_200_OK)
async def get_all_books()-> List[Book]:
	data = read_json()
	return data


@app.get("/{id}",status_code=status.HTTP_200_OK)
async def get_book(id:int)-> List[Book]:
	data = read_json()
	ob = [obj for obj in data if obj.get('id')==id]
	if not ob:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
	return ob
