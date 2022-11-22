from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

from app.forms import PostForm

from app.models.posts import Post

from app.utils.utils import Permission

from app.db import db

bp_index = Blueprint("index", __name__)


@bp_index.route("/", methods=["GET", "POST"])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("index.index"))

    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template("index.html", form=form, posts=posts, WRITE=Permission.WRITE)




