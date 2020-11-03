from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db
from .forms import PostEditForm


bp = Blueprint('', __name__, url_prefix='/')


@bp.route('/')
def index():
    db = get_db()
    # posts = db.execute(
    #     'SELECT p.id, title, body, created, author_id, username'
    #     ' FROM post p JOIN user u ON p.author_id = u.id'
    #     ' ORDER BY created DESC'
    # ).fetchall()

    # return render_template('post/index.html', posts=posts)
    return render_template('post/index.html')


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    form = PostEditForm()
    if form.validate_on_submit():
        print(form.content)
        if request.method == 'POST':
            title = request.form['content']
            # body = request.form['body']
            # error = None
            #
            # if not title:
            #     error = 'Title is required.'
            #
            # if error is not None:
            #     flash(error)
            # else:
            #     db = get_db()
            #     db.execute(
            #         'INSERT INTO post (title, body, author_id)'
            #         ' VALUES (?, ?, ?)',
            #         (title, body, g.user['id'])
            #     )
            #     db.commit()
        return redirect(url_for('post.index'))

    return render_template('post/create.html', form=form)


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        # abort() will raise a special exception that returns an HTTP status code
        # an optional message to show with the error
        #  404 means 'Not Found'
        abort(404, "Post id {0} doesn't exist.".format(id))

    # the function can be used to get a post without checking the author
    # to show an individual post on a page, not modifying the post.
    if check_author and post['author_id'] != g.user['id']:
        # 403 means 'Forbidden'
        abort(403)

    return post


# if don’t specify int: and instead do <id>, it will be a string.
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('post.index'))

    return render_template('post/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('post.index'))
