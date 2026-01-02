from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
import json
from typing import List,Dict,Optional

class Book(BaseModel):
	id: int
	title: str
	author: str

class CreateBook(BaseModel):
	title: str
	author: str

class UpdateBook(BaseModel):
	title: Optional[str] = None
	author: Optional[str] = None

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

# path param and query param
@app.get("/sorted/{author}")
async def sorted_book(author:str,field:str)->List[str]:
	data = read_json()
	ob = [obj for obj in data if obj.get('author')==author]
	result = [value.get(field) for value in ob]
	if not result:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
	return result

@app.post("/book")
async def load_book(record:CreateBook):
	data = read_json()
	print("data", data)
	id = len(data) + 1
	book_dict = {"id": id, "title": record.title, "author": record.author}
	data.append(book_dict)
	print(data)
	with open("./json_data.json","w") as f:
		json.dump(data, f, indent=4)
	return read_json()


@app.put("/update_book/{id}")
async def update_book(id:int,record: UpdateBook):
	data = read_json()
	flag = False
	for ob in data:
		if ob.get("id") == id:
			flag = True
			if record.title:
				ob["title"] = record.title
			if record.author:	
				ob["author"] = record.author
			break
	if flag:
		with open("./json_data.json","w") as f:
			json.dump(data, f, indent=4)
		return read_json()
	else:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Resource not available")

