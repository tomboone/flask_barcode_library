"""
Book model
"""
from typing import TYPE_CHECKING
from sqlalchemy import String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db

if TYPE_CHECKING:
    from flask_sqlalchemy.model import Model
else:
    Model = db.Model


class Book(Model):  # pylint: disable=too-few-public-methods
    """
    Book model
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    isbn: Mapped[int] = mapped_column(BigInteger, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=True)
    callnumber: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self):
        return f'<Book {self.author}, {self.title}>'

    @staticmethod
    def get_all_books_with_callnumbers():
        """
        Get books

        :return: all book objects
        """
        return db.session.execute(
            db.select(Book).filter(Book.callnumber != '').order_by(Book.callnumber)
        ).scalars().all()

    @staticmethod
    def get_books_missing_callnumbers():
        """
        Get books missing call numbers

        :return: books missing call numbers
        """
        return db.session.execute(
            db.select(Book).filter(Book.callnumber == '').order_by(Book.title)
        ).scalars().all()

    @staticmethod
    def get_book_by_isbn(isbn):
        """
        Get book

        :param:isbn: ISBN
        :return: book object
        """
        return db.session.execute(db.select(Book).filter_by(isbn=isbn)).scalar_one_or_none()
