from flask import Blueprint, render_template, url_for, redirect, request
from flask_login import current_user, login_required

from apps.main import db
from apps.container.forms import ContainerForm
from apps.container.models import Containers
from apps.resource.models import ResourceGroups
from apps.network.models import Networks

# gRPC
import grpc
from api import container_pb2
from api import container_pb2_grpc

container = Blueprint(
    "container",
    __name__,
    template_folder="templates",
    static_folder="static"
)

@container.route("/", methods=["GET", "POST"])
@login_required
def index():
    form = ContainerForm()
    containers = Containers.query.join(ResourceGroups).filter(ResourceGroups.user_id==current_user.id)
    # コンテナの状態(status)、IPアドレス(ip)はwataame-computeから動的に取得
    infos=[]
    with grpc.insecure_channel('localhost:8082') as ch:
        stub = container_pb2_grpc.ContainerStub(ch)
        for c in containers:
            net = Networks.query.filter(Networks.uuid==c.network_uuid).first()
            docknetid = net.docknetid
            infos.append({
                'status': stub.getStatus(container_pb2.IPRequest(id=c.id)).message,
                'ip': stub.getIP(container_pb2.IPRequest(id=c.id, docknetid=docknetid)).message
            })
    if request.method == "POST":
        id = request.form.get("id")
        action = request.form.get("action")
        if action == "create":
            return redirect(url_for("container.create"))
        elif action == "start":
            with grpc.insecure_channel('localhost:8082') as ch:
                stub = container_pb2_grpc.ContainerStub(ch)
                reply = stub.start(container_pb2.StartRequest(id=id))
            print("Reply: %s" % reply.message)
        elif action == "stop":
            with grpc.insecure_channel('localhost:8082') as ch:
                stub = container_pb2_grpc.ContainerStub(ch)
                reply = stub.stop(container_pb2.StopRequest(id=id))
            print("Reply: %s" % reply.message)
        elif action == "delete":
            with grpc.insecure_channel('localhost:8082') as ch:
                stub = container_pb2_grpc.ContainerStub(ch)
                reply = stub.delete(container_pb2.DeleteRequest(id=id))
            print("Reply: %s" % reply.message)
            cont = Containers.query.filter_by(id=id).first()
            db.session.delete(cont)
            db.session.commit()
    return render_template("container/index.html", form=form, containers=containers, infos=infos, zip=zip)

@container.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = ContainerForm()
    form.resource_group_uuid.choices = [
        (rg.uuid, rg.name) for rg in ResourceGroups.query.filter(ResourceGroups.user_id==current_user.id)
    ]
    form.network_uuid.choices = [
        (nw.uuid, nw.name) for nw in Networks.query.join(ResourceGroups).filter(ResourceGroups.user_id==current_user.id)
    ]
    if form.validate_on_submit():
        net = Networks.query.filter(Networks.uuid==form.network_uuid.data).first()
        docknetid = net.docknetid
        with grpc.insecure_channel('localhost:8082') as ch:
            stub = container_pb2_grpc.ContainerStub(ch)
            reply = stub.create(container_pb2.CreateRequest(
                name=form.name.data,
                image=form.image.data,
                docknetid=docknetid))
        cont = Containers(
            id=reply.message,
            name=form.name.data,
            resource_group_uuid=form.resource_group_uuid.data,
            network_uuid=form.network_uuid.data,
            image=form.image.data,
        )
        print("Reply: %s" % reply.message)
        db.session.add(cont)
        db.session.commit()
        return redirect(url_for("container.index"))
    return render_template("container/create.html", form=form)