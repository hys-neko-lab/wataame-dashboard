import uuid
from flask import Blueprint, render_template, url_for, redirect, request
from flask_login import current_user, login_required

from apps.main import db
from apps.resource.forms import ResourceForm
from apps.resource.models import ResourceGroups

# Blueprintの設定
resource = Blueprint(
    "resource",
    __name__,
    template_folder="templates",
    static_folder = "static"
)

@resource.route("/", methods=["GET","POST"])
@login_required
def index():
    form = ResourceForm()
    # ログインユーザが作成したリソースグループを取得
    resource_groups = ResourceGroups.query.filter(ResourceGroups.user_id==current_user.id)
    if request.method == "POST":
        # index.htmlのactionによって処理分岐
        action = request.form.get("action")
        if action == "create":
            return redirect(url_for("resource.create"))
        elif action == "delete":
            resource = ResourceGroups.query.filter_by(uuid=request.form.get("uuid")).first()
            db.session.delete(resource)
            db.session.commit()
    # GETのときはresource/index.htmlを返す
    return render_template("resource/index.html", form=form, resource_groups=resource_groups)

@resource.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = ResourceForm()
    # フォーム内容に問題なければデータベースにリソースグループを追加
    if form.validate_on_submit():
        resource = ResourceGroups(
            uuid=uuid.uuid4(),
            user_id=current_user.id,
            name=form.name.data,
        )
        db.session.add(resource)
        db.session.commit()
        return redirect(url_for("resource.index"))
    # GETのときはresource/create.htmlを返す
    return render_template("resource/create.html", form=form)