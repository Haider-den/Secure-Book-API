from . import models, database, utils
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db, username: str):
    return db.query(models.User).filter(models.User.username==username).first()

def create_user(db, username: str, password: str, roles: list[str] | None = None):
    hashed = pwd_context.hash(password)
    r = ','.join(roles) if roles else 'reader'
    user = models.User(username=username, hashed_password=hashed, roles=r)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not pwd_context.verify(password, user.hashed_password):
        return None
    # attach roles as list
    user.roles = user.roles.split(',') if isinstance(user.roles, str) else user.roles
    return user

def create_demo_users_if_not_exist(db):
    # If there are no users, create admin, writer, reader users
    if db.query(models.User).count() == 0:
        create_user(db, "admin", "adminpass", roles=["admin","writer","reader"])
        create_user(db, "writer", "writerpass", roles=["writer","reader"])
        create_user(db, "reader", "readerpass", roles=["reader"])

def create_book(db, title, author, summary):
    book = models.Book(title=title, author=author, summary=summary)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

def get_books(db, skip=0, limit=100):
    return db.query(models.Book).offset(skip).limit(limit).all()

def delete_book(db, book_id):
    b = db.query(models.Book).filter(models.Book.id==book_id).first()
    if not b:
        return False
    db.delete(b)
    db.commit()
    return True
