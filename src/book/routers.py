from fastapi import FastAPI,APIRouter, status, HTTPException
from pydantic import BaseModel
import json
from typing import List,Dict
from .schemas import Book, CreateBook, UpdateBook, PartialBook
import os
json_path = os.path.join(os.path.dirname(__file__),'json_data.json')

router = APIRouter()


def read_json()->List[Dict[str,str]]:
	contents = []
	try:
		with open(json_path,"r") as f:
			contents = json.load(f)
			print("Found data...",type(contents))
			return contents
	except FileNotFoundError:
		print("File not found.")
		return []
	except json.JSONDecodeError:
		print("Error: Invalid JSON format")
		return []


@router.get("/",status_code=status.HTTP_200_OK)
async def get_all_books()-> List[Book]:
	data = read_json()
	return data


@router.get("/{id}",status_code=status.HTTP_200_OK)
async def get_book(id:int)-> List[Book]:
	data = read_json()
	ob = [obj for obj in data if obj.get('id')==id]
	if not ob:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
	return ob

# path param and query param
@router.get("/sorted/{author}")
async def sorted_book(author:str,field:str)->List[str]:
	data = read_json()
	ob = [obj for obj in data if obj.get('author')==author]
	result = [value.get(field) for value in ob]
	if not result:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
	return result

@router.post("/book")
async def load_book(record:CreateBook):
	data = read_json()
	id = len(data) + 1
	book_dict = {"id": id, "title": record.title, "author": record.author}
	data.append(book_dict)
	with open("./json_data.json","w") as f:
		json.dump(data, f, indent=4)
	return read_json()


@router.put("/book/{id}")
async def update_book(id:int, record: UpdateBook):
	data = read_json()
	flag = False
	for ob in data:
		if ob.get("id") == id:
			flag = True
			if record.title is not None:
				ob["title"] = record.title
			if record.author is not None:	
				ob["author"] = record.author
			break
	if flag:
		with open("./json_data.json","w") as f:
			json.dump(data, f, indent=4)
		return read_json()
	else:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not available")


@router.patch("/book/{id}")
async def patch_book(id: int, record: PartialBook):
	data = read_json()
	flag = False
	for ob in data:
		if ob.get("id") == id:
			flag = True
			if record.title is not None:
				ob["title"] = record.title
			if record.author is not None:	
				ob["author"] = record.author
			break
	if flag:
		with open("./json_data.json","w") as f:
			json.dump(data, f, indent=4)
		return read_json()
	else:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not available")


@router.delete("/book/{id}")
async def delete_book(id: int):
	data = read_json()
	flag = False
	for i, ob in enumerate(data):
		if ob.get("id") == id:
			flag = True
			data.pop(i)
			break
	if flag:
		with open("./json_data.json","w") as f:
			json.dump(data, f, indent=4)
		return {"message": "Book deleted successfully"}
	else:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")