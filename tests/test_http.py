"""렌더링·폼 오류·등록·조회·수정·삭제의 HTTP 계약을 검증한다."""

import pytest

pytestmark = pytest.mark.smoke


def test_public_pages_and_form_validation(client):
    assert client.get("/").status_code == 200
    assert client.get("/books").status_code == 200
    assert client.get("/books/new").status_code == 200
    invalid = client.post(
        "/books", data={"title": "", "author": "", "publication_year": "0"}
    )
    assert invalid.status_code == 400


def test_book_crud_and_search(client):
    form = {
        "title": "검증 도서",
        "author": "검증 작성자",
        "publication_year": "2024",
        "note": "임시 데이터",
    }
    created = client.post("/books", data=form, follow_redirects=False)
    assert created.status_code == 303
    location = created.headers["location"]
    assert "검증 도서" in client.get(location).text
    form["title"] = "수정한 도서"
    assert (
        client.post(location + "/edit", data=form, follow_redirects=False).status_code
        == 303
    )
    assert "수정한 도서" in client.get("/books?q=수정한").text
    assert client.post(location + "/delete", follow_redirects=False).status_code == 303
    assert client.get(location).status_code == 404


@pytest.mark.parametrize("book_id", ["invalid", "0", "-1", "999999"])
def test_missing_or_invalid_ids_never_modify_books(client, book_id):
    for suffix in ["", "/edit"]:
        assert client.get(f"/books/{book_id}{suffix}").status_code == 404
    for suffix in ["/edit", "/delete"]:
        assert client.post(f"/books/{book_id}{suffix}").status_code == 404
    assert "등록된 도서가 없습니다" in client.get("/books").text


def test_invalid_edit_preserves_saved_values_and_renders_errors(client):
    form = {
        "title": "원래 제목",
        "author": "원래 저자",
        "publication_year": "2024",
        "note": "원래 메모",
    }
    location = client.post("/books", data=form, follow_redirects=False).headers[
        "location"
    ]
    invalid = client.post(
        location + "/edit",
        data={
            "title": " ",
            "author": "",
            "publication_year": "2101",
            "note": "가" * 1001,
        },
    )
    assert invalid.status_code == 400
    for message in ["제목은 필수", "저자는 필수", "출판년도가 너무", "1000자 이내"]:
        assert message in invalid.text
    saved = client.get(location)
    for value in form.values():
        assert value in saved.text


@pytest.mark.parametrize("query", ["검색 저자", "검색 메모", "  검색 저자  "])
def test_search_matches_author_or_note_and_excludes_other_books(client, query):
    for title, author, note in [
        ("찾을 도서", "검색 저자", "검색 메모"),
        ("제외할 도서", "다른 저자", "다른 메모"),
    ]:
        client.post(
            "/books",
            data={
                "title": title,
                "author": author,
                "note": note,
                "publication_year": "2024",
            },
        )
    response = client.get("/books", params={"q": query})
    assert response.status_code == 200
    assert "찾을 도서" in response.text
    assert "제외할 도서" not in response.text
