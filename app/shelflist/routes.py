"""
Shelflist routes
"""
from flask import Blueprint, render_template
from flask_login import login_required  # type: ignore
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
    return render_template('shelflist/index.html', shelflist=shelflist)
