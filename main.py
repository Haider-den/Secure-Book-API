import os
import logging
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse
from . import models, schemas, crud, auth, database, rate_limit, utils

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("securebook")

app = FastAPI(title="SecureBook API (Demo)")

# Create DB tables and demo users
@app.on_event("startup")
async def startup_event():
    database.Base.metadata.create_all(bind=database.engine)
    crud.create_demo_users_if_not_exist(database.SessionLocal())
    logger.info(utils.json_log({"event":"startup","status":"ok"}))

# Simple root
@app.get("/", tags=["root"])
async def root():
    return {"message": "SecureBook API. Visit /docs for interactive API docs."}

@app.post("/auth/token", response_model=schemas.Token, tags=["auth"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), request: Request = None):
    ip = request.client.host if request else "local"
    if not rate_limit.allow_request(ip, "auth", limit=10, window_seconds=60):
        raise HTTPException(status_code=429, detail="Too many auth requests, slow down.")
    user = crud.authenticate_user(database.SessionLocal(), form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": user.username, "roles": ",".join(user.roles)})
    return {"access_token": access_token, "token_type": "bearer"}

# Books endpoints
@app.post("/books", response_model=schemas.BookOut, tags=["books"])
async def create_book(book_in: schemas.BookCreate, current_user=Depends(auth.get_current_user)):
    # RBAC: require writer role
    if "writer" not in current_user.roles:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    db = database.SessionLocal()
    b = crud.create_book(db, book_in.title, book_in.author, book_in.summary)
    logger.info(utils.json_log({"event":"create_book","user":current_user.username,"book_id":b.id}))
    return b

@app.get("/books", response_model=list[schemas.BookOut], tags=["books"])
async def list_books(skip: int = 0, limit: int = 100, current_user=Depends(auth.get_current_user)):
    db = database.SessionLocal()
    books = crud.get_books(db, skip=skip, limit=limit)
    return books

@app.delete("/books/{book_id}", tags=["books"])
async def delete_book(book_id: int, current_user=Depends(auth.get_current_user)):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=403, detail="Admin role required")
    db = database.SessionLocal()
    success = crud.delete_book(db, book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    logger.info(utils.json_log({"event":"delete_book","user":current_user.username,"book_id":book_id}))
    return JSONResponse({"message":"deleted"})
