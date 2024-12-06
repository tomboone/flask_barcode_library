"""
This module initializes the Flask app and the database
"""
import click
from flask import Flask, redirect, url_for, render_template
from flask.cli import FlaskGroup, with_appcontext
from config import Config
from app.extensions import db, login_manager


def create_app(config_class=Config):
    """
    Create the Flask app

    :param config_class: configuration class
    :return: Flask app
    """
    application = Flask(__name__)  # Create the Flask app
    application.config.from_object(config_class)  # Load the configuration file

    # Initialize Flask extensions here
    db.init_app(application)  # Initialize the database
    login_manager.init_app(application)  # Initialize the login manager

    # Register blueprints here
    from app.home import bp as home_bp  # pylint: disable=import-outside-toplevel
    application.register_blueprint(home_bp)

    from app.scanner import bp as scanner_bp  # pylint: disable=import-outside-toplevel
    application.register_blueprint(scanner_bp)

    from app.user import bp as user_bp  # pylint: disable=import-outside-toplevel
    application.register_blueprint(user_bp)

    from app.shelflist import bp as shelflist_bp  # pylint: disable=import-outside-toplevel
    application.register_blueprint(shelflist_bp)

    @login_manager.user_loader
    def load_user(user_id):
        """Load user
        """
        # pylint: disable=unused-import,import-outside-toplevel
        from app.models import user  # noqa: F401
        return db.session.execute(db.select(user.User).filter_by(id=user_id)).scalar_one_or_none()

    @login_manager.unauthorized_handler
    def unauthorized():
        """
        Unauthorized handler

        :return: redirect to login page
        """
        return redirect(url_for('user.login'))

    application.cli.add_command(initdb)
    application.cli.add_command(createuser)

    @application.shell_context_processor
    def shell_context():
        """
        Shell context

        :return: shell context
        """
        return {'app': application, 'db': db}

    @application.errorhandler(404)
    def page_not_found(e):
        """
        404 error handler

        :param e: error
        :return: 404 error page
        """
        return render_template('404.html', e=e), 404

    return application


cli = FlaskGroup(create_app=create_app)


@cli.command(name='initdb')
@with_appcontext
def initdb():
    """Initialize the database
    """
    # pylint: disable=import-outside-toplevel,unused-import
    from app.models.user import User    # noqa: F401
    db.create_all()
    print('Database initialized')


@cli.command(name='createuser')
@click.option('-e', '--email', required=True, type=str)
@click.option('-p', '--password', required=True, type=str)
@with_appcontext
def createuser(email, password):
    """Create a user
    """
    from app.models.user import User  # pylint: disable=import-outside-toplevel
    user = User(email, password)
    db.session.add(user)
    db.session.commit()
    print(f'User {user.email} created')
