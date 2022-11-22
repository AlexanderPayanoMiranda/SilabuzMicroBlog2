from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user

from werkzeug.urls import url_parse

from app.db import db
from app.forms import LoginForm, EditProfileForm

from app.models.usuarios import User
from app.models.posts import Post

bp_user = Blueprint("user", __name__)


@bp_user.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("user.no_existe"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        print(type(next_page))
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index.index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)


@bp_user.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index.index"))


@bp_user.route("/no-existe")
def no_existe():
    return render_template("nouser.html")


@bp_user.route('/usuario/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template("user.html", user=user)


@bp_user.route('/edit-profile', methods=["GET", "POST"])
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash("Tu perfil se actualizo correctamente!")
        return redirect(url_for(".user.user", username=current_user.username))

    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template("edit_profile.html", form=form)


@bp_user.route("/profile")
def profile():
    post_count = Post.query.filter_by(user_id=current_user.id).count()
    return render_template("profile.html", post_count=post_count)


@bp_user.route("/ejemplo/insert")
def insert():
    u = User(username="marcelo", email="marcelo@mail1.com")
    u.set_password("1301")
    db.session.add(u)
    db.session.commit()
    return "Insertado"