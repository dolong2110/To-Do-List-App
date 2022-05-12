from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from routers import users, todos
import consts

app = FastAPI(title="To do list app",
              description="FastAPI, and to do app demo",
              version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=consts.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix=consts.v1_prefix)
app.include_router(todos.router, prefix=consts.v1_prefix)