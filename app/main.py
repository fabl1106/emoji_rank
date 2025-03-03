import sys
import os

# 모듈 경로를 못찾는 경우가 있어서 sys.path 에 경로 추가 (IDE를 사용하면 잘 찾음)
script_dir = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(script_dir) not in sys.path:
    sys.path.insert(0, os.path.dirname(script_dir))

from typing import Optional

from fastapi import FastAPI, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from services import SlackService
from conf.database import get_db, engine, Base
from app import crud, schemas


# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post(path="/slack")
async def slack(request: Request, db: Session = Depends(get_db)):
    request_event = await request.json()
    slack_service = SlackService()
    response = slack_service.check_challenge(request_event, db)

    return response


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, item_user=user.slack_id)

    if db_user:
        raise HTTPException(status_code=400, detail="already registered")

    return crud.create_user(db=db, user=user)


@app.get("/users/")
def get_user(db: Session = Depends(get_db), year: Optional[int] = None, month: Optional[int] = None):
    db_user = crud.get_users(db, year, month)

    if not db_user:
        raise HTTPException(status_code=404, detail="Does Not Exists (User)")

    return db_user


@app.get("/")
def read_root():
    return {"Hello": "World"}
