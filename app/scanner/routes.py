"""
Scanner routes
"""
from flask import Blueprint, render_template
from flask_login import login_required  # type: ignore

bp = Blueprint('scanner', __name__, url_prefix='/scanner', template_folder='templates/scanner')


@bp.route('/')
@login_required
def index():
    """
    Scanner index

    :return: scanner page
    """
    return render_template('index.html')
