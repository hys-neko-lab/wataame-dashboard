import uuid
from flask import Blueprint, render_template, url_for, redirect, request
from flask_login import current_user, login_required

from apps.main import db

from apps.storage.forms import StoragePoolForm, VolumeForm
from apps.storage.models import StoragePools, Volumes
from apps.resource.models import ResourceGroups

# gRPC
import grpc
from api import storage_pb2
from api import storage_pb2_grpc

storage = Blueprint(
    "storage",
    __name__,
    template_folder="templates",
    static_folder="static"
)

@storage.route("/", methods=["GET", "POST"])
@login_required
def index():
    # 本書では実装の時短のためストレージプールとボリュームを
    # 1ページで表示しているが、普通は分けたほうが無難
    form = StoragePoolForm()
    vform = VolumeForm()
    pools = StoragePools.query.join(ResourceGroups).filter(ResourceGroups.user_id==current_user.id)
    volumes = Volumes.query.join(pools)
    if request.method == "POST":
        uuid = request.form.get("uuid")
        vuuid = request.form.get("vuuid")
        action = request.form.get("action")
        if action == "create":
            return redirect(url_for("storage.createPool"))
        elif action == "delete":
            with grpc.insecure_channel('localhost:8083') as ch:
                stub = storage_pb2_grpc.StorageStub(ch)
                reply = stub.deletePool(storage_pb2.DeletePoolRequest(uuid=uuid))
            print("Reply: %s" % reply.message)
            pool = StoragePools.query.filter_by(uuid=uuid).first()
            db.session.delete(pool)
            db.session.commit()
        elif action == "volcreate":
            return redirect(url_for("storage.createVolume"))
        elif action == "voldelete":
            vol = Volumes.query.filter_by(uuid=vuuid).first()
            with grpc.insecure_channel('localhost:8083') as ch:
                stub = storage_pb2_grpc.StorageStub(ch)
                reply = stub.deleteVolume(storage_pb2.DeleteVolumeRequest(path=vol.path))
            print("Reply: %s" % reply.message)
            db.session.delete(vol)
            db.session.commit()
    return render_template("storage/index.html", form=form, vform=vform, pools=pools, volumes=volumes)

@storage.route("/create-pool", methods=["GET", "POST"])
@login_required
def createPool():
    # ストレージプールの作成
    form = StoragePoolForm()
    form.resource_group_uuid.choices = [
        (rg.uuid, rg.name) for rg in ResourceGroups.query.filter(ResourceGroups.user_id==current_user.id)
    ]
    if form.validate_on_submit():
        pool = StoragePools(
            uuid=uuid.uuid4(),
            resource_group_uuid=form.resource_group_uuid.data,
            name=form.name.data,
            capacity=form.capacity.data
        )
        with grpc.insecure_channel('localhost:8083') as ch:
            stub = storage_pb2_grpc.StorageStub(ch)
            reply = stub.createPool(storage_pb2.CreatePoolRequest(
                name=pool.name,
                uuid=str(pool.uuid),
                cap=pool.capacity,
                alloc=pool.capacity
            ))
        print("Reply: %s" % reply.message)
        db.session.add(pool)
        db.session.commit()
        return redirect(url_for("storage.index"))
    return render_template("storage/create.html",form=form)

@storage.route("/create-volume", methods=["GET", "POST"])
@login_required
def createVolume():
    # ボリュームの作成
    form = VolumeForm()
    form.storage_pool_uuid.choices = [
        (rg.uuid, rg.name) for rg in StoragePools.query.join(ResourceGroups).filter(ResourceGroups.user_id==current_user.id)
    ]
    if form.validate_on_submit():
        volume = Volumes(
            uuid=uuid.uuid4(),
            storage_pool_uuid=form.storage_pool_uuid.data,
            name=form.name.data,
            capacity=form.capacity.data,
            path=None
        )
        with grpc.insecure_channel('localhost:8083') as ch:
            stub = storage_pb2_grpc.StorageStub(ch)
            reply = stub.createVolume(storage_pb2.CreateVolumeRequest(
                name=volume.name,
                cap=volume.capacity,
                alloc=0,
                pooluuid=str(volume.storage_pool_uuid),
            ))
        print("Reply: %s" % reply.message)
        volume.path = reply.message
        db.session.add(volume)
        db.session.commit()
        return redirect(url_for("storage.index"))
    return render_template("storage/create-volume.html",form=form)