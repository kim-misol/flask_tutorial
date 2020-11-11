from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, make_response
)
from flaskr.auth import login_required
from flask_login import current_user
from .forms import PostEditForm, PostCreateForm
from .models import Post, User
from . import crontab, db, login_manager
from sqlalchemy import func, or_
import json
# to save img file
import uuid
from PIL import Image
from io import BytesIO
import re, base64

bp = Blueprint('post', __name__, url_prefix='/')
login_manager.login_view = "login"


@bp.route('/posts', methods=['GET'])
@login_required
def get_posts():
    posts = Post.query.all()
    return render_template('post/index.html', posts=posts)

@bp.route('/posts', methods=['POST'])
@login_required
def create_post():
    form = PostEditForm()
    if form.validate_on_submit():
        data = request.form
        title = form.title.data
        content = data['content']
        content_preview = data['content_preview']
        # attachment = data['attachment']
        attachment = ""
        save_type = data['save_type']
        content_json = data['content_json']
        content_json = json.loads(content_json)
        # check if img is in content_json
        for item in content_json['ops']:
            insert = item['insert']
            # try except
            if isinstance(insert, dict) and 'image' in insert:
                base64_data = insert['image']
                file_url = saveImgFromBase64(base64_data)
                insert['image'] = file_url

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
            return make_response(jsonify({'redirect': url_for('post.get_posts')}))
    return make_response(jsonify({'error': 'failed to create a post'}))


@bp.route('/posts/<int:post_id>', methods=['GET'])
@login_required
def load(post_id):
    # if click post, it needs to be passed correct post_id (currently, it's hard coded)
    print(f"post_id: {post_id}")
    post = Post.query.filter_by(id=post_id).first_or_404()
    if post is None:
        return redirect(url_for('.get_posts'))

    return render_template('post/index.html', post=post)


def saveImgFromBase64(codec, image_path="dev/flask_tutorial/flaskr/uploads/"):
    base64_data = re.sub('^data:image/.+;base64,', '', codec)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    random_filename = str(uuid.uuid4())
    file_url = image_path + random_filename + '.png'
    img.save(file_url, "PNG")
    return file_url


@bp.route('/posts/new', methods=('GET',))
@login_required
def create():
    form = PostEditForm()

    return render_template('post/create.html', form=form)


