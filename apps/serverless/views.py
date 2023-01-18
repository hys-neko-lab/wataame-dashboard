import uuid
from flask import Blueprint, render_template, url_for, redirect, request
from flask_login import current_user, login_required

from apps.main import db

from apps.serverless.forms import ServerlessForm
from apps.serverless.models import Serverlesses
from apps.resource.models import ResourceGroups

# gRPC
import grpc

from api import serverless_pb2
from api import serverless_pb2_grpc

serverless = Blueprint(
    "serverless",
    __name__,
    template_folder="templates",
    static_folder="static"
)

@serverless.route("/", methods=["GET", "POST"])
@login_required
def index():
    form = ServerlessForm()
    sls = Serverlesses.query.join(ResourceGroups).filter(ResourceGroups.user_id==current_user.id)
    if request.method == "POST":
        uuid = request.form.get("uuid")
        action = request.form.get("action")
        if action == "create":
            return redirect(url_for("serverless.create"))
        elif action == "delete":
            sl = Serverlesses.query.filter_by(uuid=uuid).first()
            with grpc.insecure_channel('localhost:8084') as ch:
                stub = serverless_pb2_grpc.ServerlessStub(ch)
                reply = stub.deleteServerless(serverless_pb2.DeleteRequest(name=sl.name))
            print("Reply: %s" % reply.message)
            db.session.delete(sl)
            db.session.commit()
    return render_template("serverless/index.html", form=form, sls=sls)

@serverless.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = ServerlessForm()
    form.resource_group_uuid.choices = [
        (rg.uuid, rg.name) for rg in ResourceGroups.query.filter(ResourceGroups.user_id==current_user.id)
    ]
    if form.validate_on_submit():
        sls = Serverlesses(
            uuid=uuid.uuid4(),
            resource_group_uuid=form.resource_group_uuid.data,
            name=form.name.data,
            ip=None
        )
        print(form.source.data)
        with grpc.insecure_channel('localhost:8084') as ch:
            stub = serverless_pb2_grpc.ServerlessStub(ch)
            reply = stub.createServerless(serverless_pb2.CreateRequest(
                name=sls.name,
                source=form.source.data,
            ))
        # KubernetesのサービスのIPはリプライで取得
        print("Reply: %s" % reply.message)
        sls.ip = reply.message
        db.session.add(sls)
        db.session.commit()
        return redirect(url_for("serverless.index"))
    return render_template("serverless/create.html", form=form)