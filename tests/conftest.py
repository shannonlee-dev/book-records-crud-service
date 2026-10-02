"""HTTP 테스트마다 원본 DB와 분리된 SQLite 연결을 제공한다."""

import importlib

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from book_records.core import database


@pytest.fixture
def client(tmp_path, monkeypatch):
    engine = create_engine(
        f"sqlite:///{tmp_path / 'books.db'}", connect_args={"check_same_thread": False}
    )
    monkeypatch.setattr(database, "engine", engine)
    monkeypatch.setattr(database, "SessionLocal", sessionmaker(bind=engine))
    try:
        database.Base.metadata.create_all(engine)
        app = importlib.import_module("book_records.main").app
        with TestClient(app) as test_client:
            yield test_client
    finally:
        engine.dispose()
