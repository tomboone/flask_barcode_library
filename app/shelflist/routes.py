"""
Shelflist routes
"""
from flask import Blueprint, render_template, abort, flash, redirect, url_for
from flask_login import login_required  # type: ignore
from app.extensions import db
from app.models.book import Book

bp = Blueprint('shelflist', __name__, url_prefix='/shelflist')


@bp.route('/')
@login_required
def index():
    """
    Shelflist index

    :return: shelflist page
    """
    shelflist = Book.get_all_books()  # get all books
    return render_template(
        'shelflist/index.html',
        shelflist=shelflist,
        title='Library'
    )


@bp.route('/<int:book_id>')
@login_required
def delete(book_id):
    """
    Book details

    :param book_id: book id
    :return: book details
    """
    book = Book.get_book_by_isbn(book_id)

    if book is None:
        abort(404, f'Book {book_id} not found')

    db.session.delete(book)
    db.session.commit()

    flash(
        f'Book "{book.title}" deleted',
        'info'
    )

    return redirect(url_for('shelflist.index'))
