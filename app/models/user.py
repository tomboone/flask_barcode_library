"""User"""
from typing import TYPE_CHECKING
from flask_login import login_user, UserMixin  # type: ignore
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash
from app.extensions import db

if TYPE_CHECKING:
    from flask_sqlalchemy.model import Model
else:
    Model = db.Model


class User(Model, UserMixin):  # pylint: disable=too-few-public-methods
    """User model"""
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(255))

    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password)

    def __repr__(self):
        return f'<User {self.email}>'

    @staticmethod
    def user_login(email, password):
        """ User login """
        user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one_or_none()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return user
        return None

    @staticmethod
    def get_user(user_id):
        """ Get user """
        return db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one_or_none()
