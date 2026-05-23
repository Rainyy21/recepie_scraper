import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from recepie_scraper import db, scraper, main
from recepie_scraper.models import Base


@pytest.fixture
def session_factory(monkeypatch):
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine)

    monkeypatch.setattr(db, "SessionLocal", TestSession)
    monkeypatch.setattr(scraper, "SessionLocal", TestSession)
    monkeypatch.setattr(main, "SessionLocal", TestSession)
    return TestSession
