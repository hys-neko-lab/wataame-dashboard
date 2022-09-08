from flask import Blueprint, redirect, render_template, url_for, flash
from flask_login import login_user, logout_user

from apps.auth.forms import UserForm
from apps.auth.models import User
from apps.auth.forms import SigninForm
from apps.main import db

auth = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    static_folder="static"
)

@auth.route("/signup", methods=["GET","POST"])
def signup():
    form = UserForm()
    # サインアップ情報に問題なければdashboardに飛ぶ
    # ただしログインしたわけではないのでサインイン画面にリダイレクトされる
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("dashboard.index"))
    return render_template("auth/signup.html", form=form)

@auth.route("/signin", methods=["GET", "POST"])
def signin():
    form = SigninForm()
    # サインイン情報に問題なければdashboardに飛ぶ
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user != None:
            if user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for("dashboard.index"))
        flash("メールアドレスまたはパスワードが正しくありません")
    return render_template("auth/signin.html", form=form)

@auth.route("/signout")
def signout():
    # ログアウトしたらサインイン画面にリダイレクトする
    logout_user()
    return redirect(url_for("auth.signin"))