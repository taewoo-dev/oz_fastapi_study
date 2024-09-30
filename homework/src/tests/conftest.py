"""
test code 에서 사용할 설정 관리 파일
 - test code 에서 공통적으로 사용하는 설
 - fixture:가짜 데이터
 - test db -> 연결 설정(fixture)
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from fastapi.testclient import TestClient

from core.authenticate.services.authenticate_service import AuthenticateService
from core.database.connection import get_db
from core.database.orm import Base
from main import app
from users.domains.user import User


@pytest.fixture(scope="session")
def test_db():
    test_db_url = "mysql+pymysql://root:ozcoding@127.0.0.1:3308/test"

    if not database_exists(test_db_url):
        create_database(test_db_url)

    engine = create_engine(test_db_url)
    Base.metadata.create_all(engine)  # test_db table 생성

    try:
        yield engine
    finally:
        Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def test_session(test_db):
    connection = test_db.connect()

    connection.begin()
    session = sessionmaker()(bind=connection)

    yield session  # yield는 return과 비슷, session을 다 사용했다. 즉 테스트가 끝낫다면 아래로 넘어간다

    session.rollback()
    connection.close()


@pytest.fixture
def client(test_session):
    def test_get_db():
        yield test_session

    app.dependency_overrides[get_db] = test_get_db

    return TestClient(app=app)


# 장고의 setup과 유사한 측면이 있다
@pytest.fixture(scope="function", autouse=True)
def test_user(test_session):
    new_user = User.create(
        username="test_user",
        password=AuthenticateService.hash_password("test_password"),
    )
    test_session.add(new_user)
    test_session.commit()
    return
