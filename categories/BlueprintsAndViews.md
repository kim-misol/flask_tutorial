BlueprintsAndViews.md
# [Blueprints and Views](https://flask.palletsprojects.com/en/1.1.x/tutorial/views/)
A view function is the code you write to respond to requests to your application. 
Flask uses patterns to match the incoming request URL to the view that should handle it. 
The view returns data that Flask turns into an outgoing response. 
Flask can also go the other direction and generate a URL to a view based on its name and arguments.

### Create a Blueprint
A Blueprint is a way to organize a group of related views and other code. 
Rather than registering views and other code directly with an application, they are registered with a blueprint. 
Then the blueprint is registered with the application when it is available in the factory function.

Flaskr will have two blueprints, 
one for **authentication functions** 
and one for the **blog posts functions**. 
The code for each blueprint will go in a separate module. 
Since the blog needs to know about authentication, you’ll write the authentication one first.

flaskr/`auth.py`
```
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')
```

This creates a Blueprint named `'auth'`. 
Like the application object, the blueprint needs to know where it’s defined, so `__name__` is passed as the second argument. 
The `url_prefix` will be prepended to all the URLs associated with the blueprint.

Import and register the blueprint from the factory using `app.register_blueprint()`. 
Place the new code at the end of the factory function before returning the app.

flaskr/`__init__.py`
```
def create_app():
    app = ...
    # existing code omitted

    from . import auth
    app.register_blueprint(auth.bp)

    return app
```
The authentication blueprint will have views to register new users and to log in and log out.

### The First View: Register
When the user visits the `/auth/register` URL, the register view will return HTML with a form for them to fill out. 
When they submit the form, it will validate their input and either show the form again with an error message 
or create the new user and go to the login page.

For now you will just write the view code. 
On the next page, you’ll write templates to generate the HTML form.

flaskr/`auth.py`
```
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')
```
Here’s what the register view function is doing:

1. @bp.route associates the URL /register with the register view function. 
When Flask receives a request to /auth/register, it will call the register view and use the return value as the response.
2. If the user submitted the form, request.method will be 'POST'. 
In this case, start validating the input.
3. request.form is a special type of dict mapping submitted form keys and values. 
The user will input their username and password.
