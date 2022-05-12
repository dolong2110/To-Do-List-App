from typing import List

import  fastapi as _fastapi
import sqlalchemy.orm as _orm

from backend.models import schemas as _schemas
from backend.models import model as _model
from backend.services import users as _user
from backend.services import todos as _service

app = _fastapi.APIRouter()


@app.get("/api/mytodos", response_model=List[_model.ToDo])
async def get_own_todos(current_user: _model.User = _fastapi.Depends(_user.get_current_user),
             	db: _orm.Session = _fastapi.Depends(_user.get_db)):
    """return a list of TODOs owned by current user"""
    todos = _service.get_user_todos(db, current_user.id)
    return todos

@app.post("/api/todos", response_model=_model.ToDo)
async def add_a_todo(todo_data: _schemas.TpDoCreate,
          	current_user: _model.User = _fastapi.Depends(_user.get_current_user),
          	db: _orm.Session = _fastapi.Depends(_user.get_db)):
    """add a TODO"""
    todo = _service.create_todo(db, current_user, todo_data)
    return todo

@app.put("/api/todos/{todo_id}", response_model=_model.ToDo)
async def update_a_todo(todo_id: int,
             	todo_data: _schemas.ToDoUpdate,
             	current_user: _model.User = _fastapi.Depends(_user.get_current_user),
             	db: _orm.Session = _fastapi.Depends(_user.get_db)):
    """update and return TODO for given id"""
    todo = _service.get_todo(db, todo_id)
    updated_todo = _service.update_todo(db, todo_id, todo_data)
    return updated_todo

@app.delete("/api/todos/{todo_id}")
async def delete_a_meal(todo_id: int,
             	current_user: _model.User = _fastapi.Depends(_user.get_current_user),
             	db: _orm.Session = _fastapi.Depends(_user.get_db)):
    """delete TODO of given id"""
    _service.delete_todo(db, todo_id)
    return {"detail": "TODO Deleted"}