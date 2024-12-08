"""
Scanner routes
"""
from flask import Blueprint, render_template, redirect, url_for, abort, flash
from flask_login import login_required  # type: ignore
import requests  # type: ignore
from app.extensions import db
from app.forms.barcode import BarcodeForm
from app.models.book import Book

bp = Blueprint('scanner', __name__, url_prefix='/scanner')


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """
    Scanner index

    :return: scanner page
    """
    form = BarcodeForm()  # create barcode form

    if form.validate_on_submit():  # if form is submitted
        barcode = form.barcode.data  # get barcode
        return redirect(url_for('scanner.add_book', book_id=barcode))  # redirect to book page

    return render_template(
        'scanner/index.html',
        form=form,
        title='Barcode Scanner'
    )


@bp.route('/<int:book_id>')
@login_required
def add_book(book_id):
    """
    Book details

    :param book_id: book id
    :return: book details
    """
    book = Book.get_book_by_isbn(book_id)  # try to get book by ISBN

    if book is not None:  # if book exists
        flash(  # flash message
            f'Book "{book.title}" already in library',
            'info'
        )
        return redirect(url_for('scanner.index'))

    r = requests.get(  # query Open Library Search API for authors and call number
            f'https://openlibrary.org/search.json?isbn={book_id}',
            timeout=30
    )

    # noinspection PyUnboundLocalVariable
    if r.status_code != 200 or len(r.json()['docs']) == 0:  # if book not found
        abort(404, f'{book_id} not found')  # return 404

    callnumber = ''  # initialize call number
    if 'lcc_sort' in r.json()['docs'][0]:  # if call number exists
        callnumber = r.json()['docs'][0]['lcc_sort']  # get call number

    authors = ''  # initialize authors

    if len(r.json()['docs'][0]['author_name']) == 1:  # if only one author set author
        authors = r.json()['docs'][0]['author_name'][0]
    if len(r.json()['docs'][0]['author_name']) == 2:  # if two authors set authors with 'and'
        authors = f'{r.json()["docs"][0]["author_name"][0]} and {r.json()["docs"][0]["author_name"][1]}'
    if len(r.json()['docs'][0]['author_name']) > 2:  # if more than two authors set authors with commas and 'and'
        authors = ', '.join(r.json()['docs'][0]['author_name'][:-1]) + f', and {r.json()["docs"][0]["author_name"][-1]}'

    rt = requests.get(  # query Open Library ISBN API for title and subtitle
            f'https://openlibrary.org/isbn/{book_id}.json',
            timeout=30
    )

    # noinspection PyUnboundLocalVariable
    title = rt.json()['title']

    if 'subtitle' in rt.json():  # if subtitle exists
        subtitle = rt.json()['subtitle']  # get subtitle
        title = f'{title}: {subtitle}'  # combine title and subtitle

    book = Book(isbn=book_id, title=title, author=authors, callnumber=callnumber)  # create book object

    db.session.add(book)  # add book to database
    db.session.commit()  # commit changes

    flash(  # flash message
        f'Book "{book.title}" added to library',
        'success'
    )

    return redirect(url_for('scanner.index'))  # redirect to scanner page
