import os

from flask import Flask, request, render_template


def create_app(test_config=None):
    # create and configure the app
    # instance_relative_config=True 인 경우, instance directory 에 config 파일이 존재하면 그 파일로 연동
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # define and access the database
    from . import db
    db.init_app(app)

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
