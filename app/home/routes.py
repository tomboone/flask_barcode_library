"""
Home routes
"""
from flask import Blueprint, render_template
from flask_login import login_required  # type: ignore

bp = Blueprint('home', __name__)


@bp.route('/')
@login_required
def index():
    """
    Home index

    :return: home page
    """
    return render_template('home/index.html')
