"""모듈 이동 후에도 입력 검증과 CRUD 저장 규칙을 유지한다."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from book_records.core.database import Base
from book_records.services import book_service


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    engine.dispose()


def test_crud_trims_values_and_preserves_search(db):
    book, errors = book_service.create_book_from_form(
        db, "  기록  ", "  저자  ", "2024", "  메모  "
    )
    assert errors == {}
    assert (book.title, book.author, book.note) == ("기록", "저자", "메모")
    assert book_service.list_books(db, "  기록 ") == [book]
    updated, errors = book_service.update_book_from_form(
        db, book, "수정", "저자", "2025", "새 메모"
    )
    assert errors == {} and updated.id == book.id
    book_service.delete_book(db, book)
    assert book_service.get_book(db, book.id) is None


@pytest.mark.parametrize("year", ["0", "2101", "숫자 아님"])
def test_invalid_input_does_not_write(db, year):
    book, errors = book_service.create_book_from_form(db, "", "", year, "가" * 1001)
    assert book is None
    assert set(errors) == {"title", "author", "publication_year", "note"}
    assert book_service.list_books(db) == []
