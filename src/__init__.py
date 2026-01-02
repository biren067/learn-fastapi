from fastapi import FastAPI
import src.book.routers as book
version = "v1"
app = FastAPI(version=version)
app.include_router(book.router,prefix=f"/api/{version}/book")




