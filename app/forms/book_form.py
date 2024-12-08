"""
Book form
"""
from flask_wtf import FlaskForm  # type: ignore
from wtforms import IntegerField, StringField  # type: ignore
from wtforms.validators import DataRequired  # type: ignore


class BookForm(FlaskForm):
    """
    Book form
    """
    isbn = IntegerField('ISBN', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author')
    callnumber = StringField('Call Number')
