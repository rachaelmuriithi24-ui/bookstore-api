from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Session, select
from typing import List, Optional
from datetime import datetime

from database.session import engine, get_session
from models.book import Book, BookCreate, BookUpdate


app = FastAPI(
    title="Book Inventory API Rachael Murithi C027-01-0895/2024",
    version="1.0.0"
)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


# ============================================================
# CREATE BOOK
# ============================================================

@app.post("/books", response_model=Book, status_code=201)
def create_book(
    book: BookCreate,
    session: Session = Depends(get_session)
):
    existing = session.exec(
        select(Book).where(Book.isbn == book.isbn)
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="ISBN already exists"
        )

    db_book = Book(**book.model_dump())

    session.add(db_book)
    session.commit()
    session.refresh(db_book)

    return db_book


# ============================================================
# LIST BOOKS
# ============================================================

@app.get("/books", response_model=List[Book])
def list_books(
    skip: int = 0,
    limit: int = 10,
    available: Optional[bool] = None,
    author: Optional[str] = None,
    session: Session = Depends(get_session),
):

    query = select(Book)

    if available is not None:
        query = query.where(Book.available == available)

    if author:
        query = query.where(Book.author.contains(author))

    return session.exec(
        query.offset(skip).limit(limit)
    ).all()


# ============================================================
# SEARCH BOOKS
# ============================================================

@app.get("/books/search", response_model=List[Book])
def search_books(
    q: str,
    session: Session = Depends(get_session),
):

    query = select(Book).where(
        (Book.title.contains(q)) |
        (Book.author.contains(q))
    )

    return session.exec(query).all()


# ============================================================
# GET ONE BOOK
# ============================================================

@app.get("/books/{book_id}", response_model=Book)
def get_book(
    book_id: int,
    session: Session = Depends(get_session),
):

    book = session.get(Book, book_id)

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return book


# ============================================================
# UPDATE BOOK
# ============================================================

@app.patch("/books/{book_id}", response_model=Book)
def update_book(
    book_id: int,
    book_update: BookUpdate,
    session: Session = Depends(get_session),
):

    book = session.get(Book, book_id)

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    update_data = book_update.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(book, key, value)

    book.updated_at = datetime.now()

    session.add(book)
    session.commit()
    session.refresh(book)

    return book


# ============================================================
# DELETE BOOK
# ============================================================

@app.delete("/books/{book_id}", status_code=204)
def delete_book(
    book_id: int,
    session: Session = Depends(get_session),
):

    book = session.get(Book, book_id)

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    session.delete(book)
    session.commit()

    return None