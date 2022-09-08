import uuid
from flask import Blueprint, render_template, url_for, redirect, request
from flask_login import current_user, login_required

from apps.main import db
from apps.keypair.forms import KeypairForm
from apps.keypair.models import KeyPairs
from apps.resource.models import ResourceGroups

keypair = Blueprint(
    "keypair",
    __name__,
    template_folder="templates",
    static_folder = "static"
)

@keypair.route("/", methods=["GET","POST"])
@login_required
def index():
    form = KeypairForm()
    # ログインユーザが持つリソースグループに属するキーペアを取得
    keys = KeyPairs.query.join(ResourceGroups).filter(ResourceGroups.user_id==current_user.id)
    if request.method == "POST":
        action = request.form.get("action")
        if action == "create":
            return redirect(url_for("keypair.create"))
        elif action == "delete":
            key = KeyPairs.query.filter_by(uuid=request.form.get("uuid")).first()
            db.session.delete(key)
            db.session.commit()
    return render_template("keypair/index.html", form=form, keys=keys)

@keypair.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = KeypairForm()
    # SelectFieldで表示するリストを動的に生成
    # ユーザーにはnameが見えて、フォームではuuidがsubmitされる
    form.resource_group_uuid.choices = [
        (rg.uuid, rg.name) for rg in ResourceGroups.query.filter(ResourceGroups.user_id==current_user.id)
    ]
    if form.validate_on_submit():
        keypair = KeyPairs(
            uuid=uuid.uuid4(),
            resource_group_uuid=form.resource_group_uuid.data,
            name=form.name.data,
            pubkey=form.pubkey.data
        )
        db.session.add(keypair)
        db.session.commit()
        return redirect(url_for("keypair.index"))
    return render_template("keypair/create.html", form=form)