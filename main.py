from fastapi import FastAPI

from database import Base, engine
from routers import books


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Book Notes CRUD")
app.include_router(books.router)
