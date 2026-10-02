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
