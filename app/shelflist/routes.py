"""
Shelflist routes
"""
from flask import Blueprint, render_template, abort, flash, redirect, url_for, request
from flask_login import login_required  # type: ignore
from app.extensions import db
from app.forms.book_form import BookForm
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


@bp.route('/<int:isbn>', methods=['GET', 'POST'])
@login_required
def edit_book(isbn):
    """
    Book details

    :param isbn: book isbn
    :return: book details
    """
    book = Book.get_book_by_isbn(isbn)  # try to get book by ISBN

    if book is None:  # if book doesn't exist
        abort(404, f'ISBN {isbn} not found')  # return 404

    form = BookForm(obj=book)  # create form instance with book data

    if form.validate_on_submit():  # if form is submitted
        book.isbn = form.isbn.data  # update isbn
        book.title = form.title.data  # update title
        book.author = form.author.data  # update author
        book.callnumber = form.callnumber.data  # update call number

        db.session.commit()  # commit changes

        flash(  # flash success message
            f'Book "{book.title}" updated',
            'info'
        )

        return redirect(url_for('shelflist.index'))  # redirect to shelflist index

    return render_template(  # render edit page
        'shelflist/edit.html',  # template
        book=book,  # book
        form=form,  # form
        title='Edit "' + book.title + '"'  # title
    )


@bp.route('/<int:isbn>/delete', methods=['GET', 'POST'])
@login_required
def delete_book(isbn):
    """
    Book details

    :param isbn: book isbn
    :return: book details
    """
    book = Book.get_book_by_isbn(isbn)

    if book is None:
        abort(404, f'ISBN {isbn} not found')

    if request.method == 'POST':

        db.session.delete(book)
        db.session.commit()

        flash(
            f'Book "{book.title}" deleted',
            'info'
        )

        return redirect(url_for('shelflist.index'))

    return render_template(
        'shelflist/delete.html',
        book=book,
        title='Delete "' + book.title + '"'
    )
