from sqlalchemy.orm import Session

from models.book import Book
from repositories import book_repository


def list_books(db: Session, query: str | None = None) -> list[Book]:
    cleaned_query = query.strip() if query else None
    return book_repository.list_books(db, cleaned_query)


def get_book(db: Session, book_id: int) -> Book | None:
    return book_repository.get_book(db, book_id)


def validate_book_input(title: str, author: str, publication_year: str, note: str) -> dict[str, str]:
    errors: dict[str, str] = {}
    if not title.strip():
        errors["title"] = "제목은 필수입니다."
    if not author.strip():
        errors["author"] = "저자는 필수입니다."
    try:
        year = int(publication_year)
    except ValueError:
        errors["publication_year"] = "출판년도는 숫자로 입력하세요."
    else:
        if year < 1:
            errors["publication_year"] = "출판년도는 1 이상의 숫자여야 합니다."
        if year > 2100:
            errors["publication_year"] = "출판년도가 너무 큽니다."
    if len(note.strip()) > 1000:
        errors["note"] = "메모는 1000자 이내로 입력하세요."
    return errors


def create_book_from_form(
    db: Session,
    title: str,
    author: str,
    publication_year: str,
    note: str,
) -> tuple[Book | None, dict[str, str]]:
    errors = validate_book_input(title, author, publication_year, note)
    if errors:
        return None, errors
    book = book_repository.create_book(
        db,
        title=title.strip(),
        author=author.strip(),
        publication_year=int(publication_year),
        note=note.strip(),
    )
    return book, {}


def update_book_from_form(
    db: Session,
    book: Book,
    title: str,
    author: str,
    publication_year: str,
    note: str,
) -> tuple[Book | None, dict[str, str]]:
    errors = validate_book_input(title, author, publication_year, note)
    if errors:
        return None, errors
    updated = book_repository.update_book(
        db,
        book=book,
        title=title.strip(),
        author=author.strip(),
        publication_year=int(publication_year),
        note=note.strip(),
    )
    return updated, {}


def delete_book(db: Session, book: Book) -> None:
    book_repository.delete_book(db, book)
