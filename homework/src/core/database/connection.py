from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings


# 데이터베이스에 접근,설정을 관리하는 객체
engine = create_engine(settings.database_url)

# 세션을 생성하는 객체
SessionFactory = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine,
)


# 의존성 주입을 위한 함수
def get_db():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()
