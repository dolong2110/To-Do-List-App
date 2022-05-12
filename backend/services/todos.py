import sqlalchemy.orm as _orm

from backend.models import model as _model
from backend.models import schemas as _schemas


async def create_todo(db: _orm.Session, current_user: _model.User, todo_data: _schemas.ToDoCreate):
    todo = _model.ToDo(description=todo_data.text,
                       completed=todo_data.completed)
    todo.owner = current_user
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

async def update_todo(db: _orm.Session, todo_data: _schemas.ToDoUpdate):
    todo = db.query(_model.ToDo).filter(_model.ToDo.id == id).first()
    todo.text = todo_data.text
    todo.completed = todo.completed
    db.commit()
    db.refresh(todo)
    return todo


async def delete_todo(db: _orm.Session, id: int):
    todo = db.query(_model.ToDo).filter(_model.ToDo.id == id).first()
    db.delete(todo)
    db.commit()


async def get_user_todos(db: _orm.Session, userid: int):
    return db.query(_model.ToDo).filter(_model.ToDo.owner_id == userid).all()