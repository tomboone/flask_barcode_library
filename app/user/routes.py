"""
User routes
"""
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required, logout_user  # type: ignore
from app.forms.login_form import LoginForm
from app.models.user import User

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/')
def index():
    """
    User index

    :return: redirect to user profile
    """
    return redirect(
        url_for('user.profile')  # redirect to user profile
    )


@bp.route('/profile')
@login_required
def profile():
    """
    User profile

    :return: user profile
    """
    return render_template('user/profile.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    User login

    :return: login page
    """
    if current_user.is_authenticated:
        return redirect(
            url_for('user.profile')
        )

    form = LoginForm()

    if form.validate_on_submit():

        user = User.user_login(form.email.data, form.password.data)

        if user:

            flash('Login successful', 'success')

            return redirect(
                url_for('user.profile')
            )

        flash('Invalid email or password', 'error')

        return redirect(
            url_for('user.login')
        )

    return render_template('user/login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    """
    User logout

    :return: redirect to login page
    """
    logout_user()

    return render_template('logout.html')
