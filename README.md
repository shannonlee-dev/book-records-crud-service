# 도서 기록장

FastAPI, SQLAlchemy, SQLite, Jinja2로 만든 단일 도메인 CRUD 웹 애플리케이션입니다. 도서의 제목, 저자, 출판년도, 메모를 등록하고 목록, 상세, 수정, 삭제 화면으로 관리합니다.

## 실행 환경

- Python 3.10 이상
- fastapi
- uvicorn
- sqlalchemy
- jinja2
- python-multipart

## 설치와 실행

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

브라우저에서 `http://localhost:8000` 또는 `http://127.0.0.1:8000`으로 접속합니다.

## 화면 흐름

- `GET /`: 홈 화면
- `GET /books`: 목록과 검색
- `GET /books/new`: 등록 폼
- `POST /books`: 등록 처리 후 상세 화면으로 303 리다이렉트
- `GET /books/{book_id}`: 상세 화면
- `GET /books/{book_id}/edit`: 수정 폼
- `POST /books/{book_id}/edit`: 수정 처리 후 상세 화면으로 303 리다이렉트
- `POST /books/{book_id}/delete`: 삭제 처리 후 목록 화면으로 303 리다이렉트

## 데이터베이스 확인

서버를 한 번 실행하면 프로젝트 폴더에 `database.db`가 생성됩니다. 저장된 데이터를 Python으로 직접 확인할 수 있습니다.

```sh
python - <<'PY'
import sqlite3
conn = sqlite3.connect("database.db")
for row in conn.execute("select id, title, author, publication_year, note from books order by id"):
    print(row)
conn.close()
PY
```

## 구조

```text
main.py
database.py
models/
repositories/
services/
routers/
templates/
requirements.txt
```

라우터는 요청과 화면 전환, 서비스는 입력 검증과 비즈니스 흐름, 저장소는 SQLAlchemy Session 기반 DB 접근을 담당합니다. 로그인, 권한, 인증, 모델 간 연관관계는 구현하지 않았습니다.
