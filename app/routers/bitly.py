import validators
import secrets

from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..db import models
from ..db.database import SessionLocal, engine
from ..config import settings

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Requests(BaseModel):
    target_url: str
    is_active: bool
    clicks: int
    url: str
    admin_url: str

class FirstRequests(BaseModel):
    target_url: str

router = APIRouter()
models.Base.metadata.create_all(bind=engine)

def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)

def raise_not_found(request):
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)

@router.post("/url")
def create_url(request: FirstRequests, db: Session = Depends(get_db)):
    if not validators.url(request.target_url):
        raise_bad_request(message="Your provided URL is not valid")

    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = "".join(secrets.choice(chars) for _ in range(5))
    secret_key = "".join(secrets.choice(chars) for _ in range(8))
    db_url = models.URL(
        target_url=request.target_url, key=key, secret_key=secret_key
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    db_url.url = key
    db_url.admin_url = secret_key

    return db_url

@router.get("/{url_key}")
def endpoint_key__(url_key: str, request: Request, db: Session = Depends(get_db)):

    db_url = (
        db.query(models.URL)
        .filter(models.URL.key == url_key, models.URL.is_active)
        .first()
    )
    if db_url:
        return RedirectResponse(db_url.target_url)
        
    return raise_not_found(request)