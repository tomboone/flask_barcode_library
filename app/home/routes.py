"""
Home routes
"""
from flask import Blueprint, redirect, url_for
from flask_login import login_required  # type: ignore

bp = Blueprint('home', __name__)


@bp.route('/')
@login_required
def index():
    """
    Home index

    :return: home page
    """
    return redirect(url_for('shelflist.index'))
