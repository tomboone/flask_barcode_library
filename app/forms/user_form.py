"""
User form
"""
from flask_wtf import FlaskForm  # type: ignore
from wtforms.fields.simple import StringField, PasswordField  # type: ignore
from wtforms.validators import DataRequired, Email  # type: ignore


class UserForm(FlaskForm):
    """
    User form

    :return: user form
    """
    email = StringField(  # email field
        'Email',  # label
        validators=[DataRequired(), Email()]  # validators
    )
    password = PasswordField(  # password field
        'Password',  # label
        validators=[DataRequired()]  # validators
    )
