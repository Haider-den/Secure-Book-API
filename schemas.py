from pydantic import BaseModel, constr

class Token(BaseModel):
    access_token: str
    token_type: str

class UserBase(BaseModel):
    username: constr(min_length=3, max_length=50)

class UserCreate(UserBase):
    password: constr(min_length=6)

class BookCreate(BaseModel):
    title: constr(min_length=1, max_length=200)
    author: constr(min_length=1, max_length=100)
    summary: constr(max_length=2000) | None = None

class BookOut(BaseModel):
    id: int
    title: str
    author: str
    summary: str | None = None

    class Config:
        orm_mode = True
