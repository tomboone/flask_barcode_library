"""
Barcode form
"""
from flask_wtf import FlaskForm  # type: ignore
from wtforms.fields.simple import StringField  # type: ignore
from wtforms.validators import DataRequired  # type: ignore


class BarcodeForm(FlaskForm):
    """
    Barcode form
    """
    barcode = StringField('Barcode', validators=[DataRequired()])
