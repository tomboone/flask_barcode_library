"""
Book model
"""
from typing import TYPE_CHECKING
from sqlalchemy import String
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
    isbn: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=True)

    def __repr__(self):
        return f'<Book {self.author}, {self.title}>'

    @staticmethod
    def get_all_books():
        """
        Get books

        :return: all book objects
        """
        return db.session.execute(db.select(Book)).scalars().all()

    @staticmethod
    def get_book_by_isbn(isbn):
        """
        Get book

        :param:isbn: ISBN
        :return: book object
        """
        return db.session.execute(db.select(Book).filter_by(isbn=isbn)).scalar_one_or_none()

    @staticmethod
    def get_book_metadata(isbn):
        """
        Get book metadata

        :param:isbn: ISBN
        :return: metadata to create book object
        """
        # TODO: Query Open Library API for edition metadata
        return
