from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from models.book import Book


def list_books(db: Session, query: str | None = None) -> list[Book]:
    statement = select(Book).order_by(Book.id.desc())
    if query:
        pattern = f"%{query.strip()}%"
        statement = (
            select(Book)
            .where(or_(Book.title.like(pattern), Book.author.like(pattern), Book.note.like(pattern)))
            .order_by(Book.id.desc())
        )
    return list(db.scalars(statement))


def get_book(db: Session, book_id: int) -> Book | None:
    return db.get(Book, book_id)


def create_book(db: Session, title: str, author: str, publication_year: int, note: str) -> Book:
    book = Book(title=title, author=author, publication_year=publication_year, note=note)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def update_book(db: Session, book: Book, title: str, author: str, publication_year: int, note: str) -> Book:
    book.title = title
    book.author = author
    book.publication_year = publication_year
    book.note = note
    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book: Book) -> None:
    db.delete(book)
    db.commit()
