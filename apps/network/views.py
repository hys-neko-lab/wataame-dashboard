import random
import uuid
from flask import Blueprint, render_template, url_for, redirect, request
from flask_login import current_user, login_required

from apps.main import db
from apps.network.forms import NetworkForm, BridgeForm
from apps.network.models import Networks
from apps.resource.models import ResourceGroups

# gRPC
import grpc
from api import network_pb2
from api import network_pb2_grpc

network = Blueprint(
    "network",
    __name__,
    template_folder="templates",
    static_folder = "static"
)

@network.route("/", methods=["GET","POST"])
@login_required
def index():
    form = NetworkForm()
    networks = Networks.query.join(ResourceGroups).filter(ResourceGroups.user_id==current_user.id)
    if request.method == "POST":
        uuid = request.form.get("uuid")
        action = request.form.get("action")
        if action == "create":
            # NAT作成の場合
            return redirect(url_for("network.create"))
        elif action == "createBridge":
            # ブリッジ作成の場合
            return redirect(url_for("network.createBridge"))
        elif action == "delete":
            # POSTされたUUIDに合致するネットワーク削除をwataame-networkに依頼
            net = Networks.query.filter_by(uuid=uuid).first()
            with grpc.insecure_channel('localhost:8081') as ch:
                stub = network_pb2_grpc.NetworkStub(ch)
                reply = stub.deleteVN(network_pb2.DeleteVNRequest(uuid=uuid, docknetid=net.docknetid))
            print("Reply: %s" % reply.message)
            db.session.delete(net)
            db.session.commit()
        else:
            print(request.form.get("action"))
    return render_template("network/index.html", form=form, networks=networks)

@network.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = NetworkForm()
    form.resource_group_uuid.choices = [
        (rg.uuid, rg.name) for rg in ResourceGroups.query.filter(ResourceGroups.user_id==current_user.id)
    ]
    if form.validate_on_submit():
        # MACアドレスの上位3オクテットはベンダーコード(OUI)
        # 本書ではKVM同様52:54:00を使用。残りは乱数
        net = Networks(
            uuid=uuid.uuid4(),
            docknetid=None,
            resource_group_uuid=form.resource_group_uuid.data,
            name=form.name.data,
            cidr=form.cidr.data + '/' + str(form.netmask.data),
            type="nat",
            mac="52:54:00:%02x:%02x:%02x" % (
                random.randint(0,255),
                random.randint(0,255),
                random.randint(0,255))
        )
        # NAT作成をwataame-networkに依頼
        with grpc.insecure_channel('localhost:8081') as ch:
            stub = network_pb2_grpc.NetworkStub(ch)
            reply = stub.createVN(network_pb2.CreateVNRequest(
                name=net.name,
                uuid=str(net.uuid),
                cidr=net.cidr,
                mac=net.mac))
        # dockerネットワークのIDはgRPCのリプライでもらう
        print("Reply: %s" % reply.message)
        net.docknetid=reply.docknetid
        db.session.add(net)
        db.session.commit()
        return redirect(url_for("network.index"))
    return render_template("network/create.html", form=form)

@network.route("/create-bridge", methods=["GET", "POST"])
@login_required
def createBridge():
    form = BridgeForm()
    form.resource_group_uuid.choices = [
        (rg.uuid, rg.name) for rg in ResourceGroups.query.filter(ResourceGroups.user_id==current_user.id)
    ]
    if form.validate_on_submit():
        net = Networks(
            uuid=uuid.uuid4(),
            docknetid=None,
            resource_group_uuid=form.resource_group_uuid.data,
            name=form.name.data,
            cidr=None,
            type="bridge",
        )
        # ブリッジ作成をwataame-networkに依頼
        with grpc.insecure_channel('localhost:8081') as ch:
            stub = network_pb2_grpc.NetworkStub(ch)
            reply = stub.createBridge(network_pb2.CreateBridgeRequest(
                name=net.name,
                uuid=str(net.uuid)))
        # dockerネットワークのIDはgRPCのリプライでもらう
        print("Reply: %s" % reply.message)
        net.docknetid=reply.docknetid
        net.cidr=reply.message
        db.session.add(net)
        db.session.commit()
        return redirect(url_for("network.index"))
    return render_template("network/create-bridge.html", form=form)