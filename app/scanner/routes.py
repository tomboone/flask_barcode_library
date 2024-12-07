"""
Scanner routes
"""
from flask import Blueprint, render_template, redirect, url_for, abort
from flask_login import login_required  # type: ignore
import requests  # type: ignore
from app.forms.barcode import BarcodeForm

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
        return redirect(url_for('scanner.book', book_id=barcode))  # redirect to book page

    return render_template('scanner/index.html', form=form)  # render scanner page


@bp.route('/<int:book_id>')
@login_required
def book(book_id):
    """
    Book details

    :param book_id: book id
    :return: book details
    """
    try:
        r = requests.get(  # query Open Library API
            f'https://openlibrary.org/search.json?isbn={book_id}',
            timeout=30
        )
    except requests.exceptions.Timeout:
        abort(504, 'Request timed out')

    if r.status_code != 200 or len(r.json()['docs']) == 0:  # if book not found
        abort(404, f'{book_id} not found')  # return 404

    title = r.json()['docs'][0]['title']  # get title

    if 'subtitle' in r.json()['docs'][0]:  # if subtitle exists
        subtitle = r.json()['docs'][0]['subtitle']  # get subtitle
        title = f'{title}: {subtitle}'  # combine title and subtitle

    callnumber = r.json()['docs'][0]['lcc_sort']  # get call number

    return f'{title} ({callnumber})'  # return book details
