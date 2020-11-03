import os
from flask_bcrypt import Bcrypt
from flask_crontab import Crontab
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask import Flask, request, render_template


def create_app(config='DevelopmentConfig'):
    # create and configure the app
    # instance_relative_config=True 인 경우, instance directory 에 config 파일이 존재하면 그 파일로 연동
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(f'config.{config}')

    try:
        app.config.from_pyfile('config.py')
    except FileNotFoundError:
        pass

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # define and access the database
    # DB - sqlite
    # from . import db
    # db.init_app(app)
    # DB - postgresql
    db.init_app(app)
    from .models import init_db_command, reset_db_command
    app.cli.add_command(init_db_command)
    app.cli.add_command(reset_db_command)

    crontab.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    # post blueprint
    from . import post
    app.register_blueprint(post.bp)
    app.add_url_rule('/', endpoint='index')

    # auth blueprint
    from . import auth
    app.register_blueprint(auth.bp)

    # blog blueprint
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app


db = SQLAlchemy()
crontab = Crontab()
login_manager = LoginManager()
bcrypt = Bcrypt()
migrate = Migrate()
ma = Marshmallow()
