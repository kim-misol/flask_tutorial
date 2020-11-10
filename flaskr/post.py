from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from flaskr.auth import login_required
from flask_login import current_user
from .forms import PostEditForm, PostCreateForm
from .models import Post, User
from . import crontab, db, login_manager
from sqlalchemy import func, or_
import json

bp = Blueprint('post', __name__, url_prefix='/')
login_manager.login_view = "login"


@bp.route('/posts', methods=['GET'])
@login_required
def get_posts():
    posts = Post.query.all()
    return render_template('post/index.html', posts=posts)


@bp.route('/posts/<int:post_id>', methods=['GET'])
@login_required
def load(post_id):
    # if click post, it needs to be passed correct post_id (currently, it's hard coded)
    print(f"post_id: {post_id}")
    post = Post.query.filter_by(id=post_id).first_or_404()
    if post is None:
        return redirect(url_for('.get_posts'))

    return render_template('post/index.html', post=post)


@bp.route('/posts/new', methods=('GET', 'POST'))
@login_required
def create():
    form = PostEditForm()
    if form.validate_on_submit():
        data = request.form
        title = data['title']
        content = data['content']
        content_preview = data['content_preview']
        # attachment = data['attachment']
        attachment = ""
        save_type = data['save_type']
        content_json = data['content_json']
        content_json = json.loads(content_json)

        error = None

        if not title:
            error = 'Title is required.'
        elif not content:
            error = 'Content is required.'

        if error is not None:
            flash(error)
            return render_template('post/create.html', form=form)
        else:
            from datetime import datetime
            now = datetime.now()
            created_at = now.strftime("%Y-%m-%d %H:%M:%S")
            user_id = current_user.id
            new_post = Post(title=title, content=content, content_json=content_json,
                            content_preview=content_preview, attachment=attachment, save_type=save_type,
                            created_at=created_at, modified_at=created_at, user_id=user_id)
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('.get_posts'))

    return render_template('post/create.html', form=form)


