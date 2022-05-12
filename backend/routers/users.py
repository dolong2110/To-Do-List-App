"""Receive params as schema, calls services fnc, then respond as schema."""
from typing import List
import datetime as _dt

import fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy.orm as _orm

import backend.models.schemas as _schemas
import backend.models.model as _model
import backend.services.users as _services
from backend.config import settings

app = _fastapi.FastAPI()


@app.post("/api/v1/users")
async def create_user(
        user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    db_user = await _services.get_user_by_email(user.email, db)
    if db_user:
        raise _fastapi.HTTPException(status_code=400, detail="Email already in user")

    await _services.create_user(user, db)

    return await _services.create_access_token(user)


@app.post("/api/v1/token")
async def generate_token(
        form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
        db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    user = await _services.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Credentials")
    return await _services.create_token(user)


@app.get("/api/v1/users/me", response_model=_schemas.User)
async def get_user(user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    return user


@app.post("/api/v1/leads", response_model=_schemas.Lead)
async def create_lead(
        lead: _schemas.LeadCreate,
        user: _schemas.User = _fastapi.Depends(_services.get_current_user),
        db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    return await _services.create_lead(user=user, db=db, lead=lead)


@app.get("/api/v1/leads", response_model=List[_schemas.Lead])
async def get_leads(
        user: _schemas.User = _fastapi.Depends(_services.get_current_user),
        db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    return await _services.get_leads(user=user, db=db)


@app.get("/api/v1/leads/{lead_id}", status_code=200)
async def get_lead(
        lead_id: int,
        user: _schemas.User = _fastapi.Depends(_services.get_current_user),
        db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    return await _services.get_lead(lead_id=lead_id, user=user, db=db)


@app.delete("/api/v1/leads/{lead_id}", status_code=204)
async def delete_lead(
        lead_id: int,
        user: _schemas.User = _fastapi.Depends(_services.get_current_user),
        db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    await _services.delete_lead(lead_id, user, db)
    return {"message", "Successfully Deleted"}


@app.put("/api/v1/leads/{lead_id}", status_code=200)
async def update_lead(
        lead_id: int,
        lead: _schemas.LeadCreate,
        user: _schemas.User = _fastapi.Depends(_services.get_current_user),
        db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    await _services.update_lead(lead_id, lead, user, db)
    return {"message", "Successfully Updated"}


@app.get("/api/v1")
async def root():
    return {"message": "Awesome Leads Manager"}

@app.post("/api/users", response_model=_schemas.User)
def signup(user_data: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
   """add new user"""
   user = _services.get_user_by_email(db, user_data.email)
   if user:
   	raise _fastapi.HTTPException(status_code=409,
   	                    detail="Email already registered.")
   signedup_user = _services.create_user(db, user_data)
   return signedup_user

@app.post("/api/v1/login", response_model=_schemas.TokenData)
async def login_for_access_token(db: _orm.Session = _fastapi.Depends(_services.get_db),form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends()):
    user = _services.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise _fastapi.HTTPException(
            status_code=_fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = _dt.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = _services.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    response = {
            "access_token": access_token,
            "token_type": "bearer",
            "username": user.username}
    return response

@app.get("/api/me", response_model=_schemas.User)
async def read_logged_in_user(current_user: _model.User = _fastapi.Depends(_services.authenticate_user)):
    return current_user
