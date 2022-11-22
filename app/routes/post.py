from flask import Blueprint, url_for, request, g, jsonify, render_template
from flask_httpauth import HTTPBasicAuth

from app.models.usuarios import User
from app.models.posts import Post
from app.forms import CommentForm
from app.utils.utils import Permission
from app.utils.decorator import permission_required_rest
from app.db import db

bp_post = Blueprint("post", __name__)

auth = HTTPBasicAuth()


@bp_post.route("/postJson/", methods=["POST"])
@auth.login_required
@permission_required_rest(Permission.WRITE)
def new_post():
    post = Post.from_json(request.json)
    post.author = g.current_user

    db.session.add(post)
    db.session.commit()

    return jsonify(post.to_json()), 201, {"Location": url_for("post.post_success", id=post.id)}


# Utilitario con decorador para verificar la contrasena
@auth.verify_password
def verify_password(email, password):
    if email == "" or email is None:
        return False
    user = User.query.filter_by(email=email).first()
    if not user:
        return False
    print(user.email)
    g.current_user = user
    print(g.current_user)
    return user.check_password(password)


@bp_post.route('/post_success')
def post_success():
    return "post_success"


@bp_post.route("/post/<id>")
def post_detail(id):
    form = CommentForm()

    post = Post.query.filter_by(id=id).first()

    context = {
        "form": form,
        "post": post
    }

    return render_template("post-detail.html", **context)