from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flask_login import current_user
# from flaskr.db import get_db
from .forms import PostEditForm, PostCreateForm
from .models import Post, User
from . import crontab, db, login_manager
from sqlalchemy import func, or_

bp = Blueprint('', __name__, url_prefix='/')
login_manager.login_view = "login"


@bp.route('/', methods=['GET'])
@bp.route('/<int:page>', methods=['GET'])
@login_required
def index():
    posts = Post.query.all()
    return render_template('post/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    form = PostEditForm()
    if form.validate_on_submit():
        title = form.title
        # content = form.content
        data = request.get_json()
        # request.values
        # request.form.get('title')
        content = data.get('content')
        # error = None
        error = "test"

        if not title:
            error = 'Title is required.'
        elif not content:
            error = 'Content is required.'

        if error is not None:
            flash(error)
            return render_template('post/create.html', form=form)
        else:
            import datetime

            now = datetime.datetime.now()
            created_at = now.strftime("%Y-%m-%d %H:%M:%S")
            user_id = current_user.id
            new_post = Post(title=form.title.data, content=content, created_at=created_at, user_id=user_id)
            db.session.add(new_post)
            db.session.commit()

            return redirect(url_for('index'))

    return render_template('post/create.html', form=form)


@bp.route('/posts', methods=['GET'])
@bp.route('/posts/<int:page>', methods=['GET'])
@login_required
def get_posts(page=1):
    q = request.args.get('q')
    type_ = request.args.get('type')
    posts = db.session.query(Post).join(Post.comments, isouter=True)

    # # search query
    # if q and q.isascii():
    #     posts = posts.join(Post.user).filter(or_(User.present_name.match(q), Post.content.match(q)))
    # elif q:
    #     posts = posts.join(Post.user).filter(or_(User.present_name.like(f"%{q}%"), Post.content.like(f"%{q}%")))
    #
    # order = (Post.created_at.desc(),)
    # if type_ == '2':  # 답변 대기 목록
    #     posts = posts.filter(or_(~Post.comments.any(), Post.is_answered==False)).filter(Post.admin_id==None)
    # elif type_ == '3':  # 답변 완료 목록
    #     posts = posts.filter(Post.is_answered)
    #     order = (Comment.created_at.desc(), Post.created_at.desc())
    # elif type_ == '4':  # 패스 목록
    #     posts = posts.filter(Post.admin_id!=None)
    #     order = (Post.checked_at.desc(),)

    # total = get_count(posts)
    # post_pagination = posts.order_by(*order).paginate(page)
    query_string = {k: v for k, v in request.args.items()}

    # return render_template('index.html', posts=post_pagination.items, pagination=post_pagination, qs=query_string)
    return render_template('index.html', qs=query_string)


# def _get_post(id, check_author=True):
# post = get'_db().execute(
#     'SELECT p.id, title, body, created, author_id, username'
#     ' FROM post p JOIN user u ON p.author_id = u.id'
#     ' WHERE p.id = ?',
#     (id,)
# ).fetchone()
#
# if post is None:
#     # abort() will raise a special exception that returns an HTTP status code
#     # an optional message to show with the error
#     #  404 means 'Not Found'
#     abort(404, "Post id {0} doesn't exist.".format(id))
#
# # the function can be used to get a post without checking the author
# # to show an individual post on a page, not modifying the post.
# if check_author and post['author_id'] != g.user['id']:
#     # 403 means 'Forbidden'
#     abort(403)
#
# return post

"""
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
"""
