from fastapi import FastAPI
import src.book.routers as book
app = FastAPI(version="1.0.0")
app.include_router(book.router)




