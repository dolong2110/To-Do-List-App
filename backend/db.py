import os

from uuid import UUID

from sqlalchemy.ext.declarative import declared_attr, as_declarative

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql://root:root@127.0.0.1/todolistFastapi")

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@as_declarative()
class Base:
    _id: UUID
    __name__: str

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()
