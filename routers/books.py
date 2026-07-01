from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from services import book_service


router = APIRouter()
templates = Jinja2Templates(directory="templates")


def book_form_data(
    title: str = Form(""),
    author: str = Form(""),
    publication_year: str = Form(""),
    note: str = Form(""),
) -> dict[str, str]:
    return {
        "title": title,
        "author": author,
        "publication_year": publication_year,
        "note": note,
    }


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(request, "home.html")


@router.get("/books")
def list_books(request: Request, q: str | None = None, db: Session = Depends(get_db)):
    books = book_service.list_books(db, q)
    return templates.TemplateResponse(
        request,
        "books/list.html",
        {"books": books, "q": q or ""},
    )


@router.get("/books/new")
def new_book_form(request: Request):
    return templates.TemplateResponse(
        request,
        "books/form.html",
        {
            "mode": "create",
            "action_url": "/books",
            "book": {},
            "errors": {},
        },
    )


@router.post("/books")
def create_book(
    request: Request,
    form: dict[str, str] = Depends(book_form_data),
    db: Session = Depends(get_db),
):
    book, errors = book_service.create_book_from_form(db, **form)
    if errors:
        return templates.TemplateResponse(
            request,
            "books/form.html",
            {
                "mode": "create",
                "action_url": "/books",
                "book": form,
                "errors": errors,
            },
            status_code=400,
        )
    return RedirectResponse(url=f"/books/{book.id}", status_code=303)


@router.get("/books/{book_id}")
def book_detail(request: Request, book_id: int, db: Session = Depends(get_db)):
    book = book_service.get_book(db, book_id)
    if book is None:
        return templates.TemplateResponse(
            request,
            "books/not_found.html",
            {"book_id": book_id},
            status_code=404,
        )
    return templates.TemplateResponse(request, "books/detail.html", {"book": book})


@router.get("/books/{book_id}/edit")
def edit_book_form(request: Request, book_id: int, db: Session = Depends(get_db)):
    book = book_service.get_book(db, book_id)
    if book is None:
        return templates.TemplateResponse(
            request,
            "books/not_found.html",
            {"book_id": book_id},
            status_code=404,
        )
    return templates.TemplateResponse(
        request,
        "books/form.html",
        {
            "mode": "edit",
            "action_url": f"/books/{book.id}/edit",
            "book": book,
            "errors": {},
        },
    )


@router.post("/books/{book_id}/edit")
def update_book(
    request: Request,
    book_id: int,
    form: dict[str, str] = Depends(book_form_data),
    db: Session = Depends(get_db),
):
    book = book_service.get_book(db, book_id)
    if book is None:
        return templates.TemplateResponse(
            request,
            "books/not_found.html",
            {"book_id": book_id},
            status_code=404,
        )
    updated, errors = book_service.update_book_from_form(db, book, **form)
    if errors:
        return templates.TemplateResponse(
            request,
            "books/form.html",
            {
                "mode": "edit",
                "action_url": f"/books/{book.id}/edit",
                "book": {**form, "id": book.id},
                "errors": errors,
            },
            status_code=400,
        )
    return RedirectResponse(url=f"/books/{updated.id}", status_code=303)


@router.post("/books/{book_id}/delete")
def remove_book(book_id: int, db: Session = Depends(get_db)):
    book = book_service.get_book(db, book_id)
    if book is not None:
        book_service.delete_book(db, book)
    return RedirectResponse(url="/books", status_code=303)
