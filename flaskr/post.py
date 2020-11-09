from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from flaskr.auth import login_required
from flask_login import current_user
from .forms import PostEditForm, PostCreateForm
from .models import Post, User
from . import crontab, db, login_manager
from sqlalchemy import func, or_

bp = Blueprint('', __name__, url_prefix='/')
login_manager.login_view = "login"


@bp.route('/', methods=['GET'])
@bp.route('/<int:page>', methods=['GET'])
@login_required
def get_posts():
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


