from fastapi import FastAPI

from book_records.core.database import Base, engine
from book_records.routers import books

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Book Notes CRUD")
app.include_router(books.router)
