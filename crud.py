from sqlalchemy import select, Sequence
from sqlalchemy.orm import Session

import models
import schemas


def get_all_authors(db: Session) -> Sequence[models.DBAuthor]:
    return db.scalars(select(models.DBAuthor)).all()


def get_author_by_id(
        db: Session,
        author_id: int
):
    return db.scalar(
        select(models.DBAuthor).where(models.DBAuthor.id == author_id)
    )


def create_author(
        db: Session,
        author_info: schemas.AuthorCreate
):
    db_author = models.DBAuthor(
        name=author_info.name,
        bio=author_info.bio,
    )
    db.add(db_author)
    db.flush()

    for book in author_info.books:
        db_book = models.DBBook(
            name=book.name,
            summary=book.summary,
            publication_date=book.publication_date,
            author_id=db_author.id,
        )
        db.add(db_book)

    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def update_author(
        db: Session,
        author_id_to_update: int,
        author_update_info: schemas.AuthorUpdate
):
    author = db.get(models.DBAuthor, author_id_to_update)

    if not author:
        raise ValueError("There is no such author")

    author.name = author_update_info.name
    author.bio = author_update_info.bio
    updated_books = []
    for book in author_update_info.books:
        db_book = db.get(models.DBBook, book.id)
        if db_book:
            updated_books.append(db_book)

    author.books = updated_books

    db.commit()
    db.refresh(author)

    return author


def partial_update_author(
        db: Session,
        author_id_to_update: int,
        author_update_info: schemas.AuthorPartialUpdate
):
    author = db.get(models.DBAuthor, author_id_to_update)

    if author_update_info.name:
        author.name = author_update_info.name

    if author_update_info.bio:
        author.bio = author_update_info.bio

    if author.books:
        for book in author_update_info.books:
            db_book = db.get(models.DBBook, book.id)
            if db_book:
                author.books.append(db_book)

    db.commit()
    db.refresh(author)

    return author


def delete_author(
        db: Session,
        author_id
):
    author = db.get(models.DBAuthor, author_id)

    db.delete(instance=author)
    db.commit()

    return f"{author.name} was Successfully deleted!!!"


def get_all_books(
        db: Session
):
    return db.scalars(select(models.DBBook)).all()


def get_book_by_id(
        db: Session,
        book_id: int
):
    return db.scalar(select(models.DBBook).where(models.DBBook.id == book_id))


def create_book(
        db: Session,
        book_info: schemas.BookCreate
):
    db_book = models.DBBook(
        name=book_info.name,
        summary=book_info.summary,
        publication_date=book_info.publication_date,
        author_id=book_info.author_id
    )

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def update_book(
        db: Session,
        book_id: int,
        book_update_info: schemas.BookUpdate
):
    db_book = db.get(models.DBBook, book_id)

    db_book.name = book_update_info.name
    db_book.summary = book_update_info.summary
    db_book.publication_date = book_update_info.publication_date
    db_book.author_id = book_update_info.author_id

    db.commit()
    db.refresh(db_book)

    return db_book


def partial_update_book(
        db: Session,
        book_id: int,
        book_update_info: schemas.BookPartialUpdate
):
    db_book = db.get(models.DBBook, book_id)
    book_update_info = book_update_info.model_dump(exclude_unset=True)

    for field, value in book_update_info.items():
        setattr(db_book, field, value)

    db.commit()
    db.refresh(db_book)

    return db_book


def delete_book(
        db: Session,
        book_id: int
):
    db_book = db.get(models.DBBook, book_id)

    db.delete(db_book)
    db.commit()

    return db_book
