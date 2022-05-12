import datetime as _dt

import sqlalchemy as _sql
import sqlalchemy.orm as _orm


from backend.db import Base
from backend.utils import password as _pwd


class User(Base):
    __tablename__ = "users"
    id = _sql.Column('id', _sql.Integer, autoincrement=True, primary_key=True, index=True)
    username = _sql.Column(_sql.String, unique=True)
    first_name = _sql.Column(_sql.String, index=True)
    last_name = _sql.Column(_sql.String, index=True)
    hashed_password = _sql.Column(_sql.String)
    email = _sql.Column(_sql.String, unique=True, index=True)
    _sql.PrimaryKeyConstraint(username)

    leads = _orm.relationship("Lead", back_populates="owner")
    todos = _orm.relationship("ToDo", back_populates="owner", cascade="all, delete-orphan")

    def __repr__(self):
        return "<UserOrm(username='{0}', password='{2}')>".format(self.username, self.password)

    def verify_password(self, password: str):
        return _pwd.verify(password, self.hashed_password)


class Lead(Base):
    __tablename__ = "leads"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    owner_id = _sql.Column(_sql.Integer, _sql.ForeignKey("users.id"))
    first_name = _sql.Column(_sql.String, index=True)
    last_name = _sql.Column(_sql.String, index=True)
    email = _sql.Column(_sql.String, index=True)
    company = _sql.Column(_sql.S, index=True, default="")
    note = _sql.Column(_sql.String, default="")
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    date_last_updated = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)

    owner = _orm.relationship("User", back_populates="leads")

class ToDo(Base):
    __tablename__ = "todos"

    _id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    name = _sql.Column(_sql.String)
    description = _sql.Column(_sql.String, default="")
    completed = _sql.Column(_sql.Boolean, default=False)
    owner_id = _sql.Column(_sql.Integer, _sql.ForeignKey("users.id"))
    created_at = _sql.Column(_sql.DateTime)
    owner = _orm.relationship("User", back_populates="todos")