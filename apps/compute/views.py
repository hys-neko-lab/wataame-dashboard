import random
import uuid
import crypt
from flask import Blueprint, render_template, url_for, redirect, request
from flask_login import current_user, login_required

from apps.main import db
from apps.compute.forms import ComputeForm
from apps.compute.models import VirtualMachines, Images, MachineTypes
from apps.resource.models import ResourceGroups
from apps.network.models import Networks
from apps.keypair.models import KeyPairs
from apps.storage.models import StoragePools, Volumes

# gRPC
import grpc
from api import compute_pb2, storage_pb2
from api import compute_pb2_grpc, storage_pb2_grpc

compute = Blueprint(
    "compute",
    __name__,
    template_folder="templates",
    static_folder = "static"
)

@compute.route("/", methods=["GET","POST"])
@login_required
def index():
    form = ComputeForm()
    vms = VirtualMachines.query.join(ResourceGroups).filter(ResourceGroups.user_id==current_user.id)
    # 仮想マシンの状態(status)、IPアドレス(ip)はwataame-computeから動的に取得
    infos=[]
    with grpc.insecure_channel('localhost:8080') as ch:
        stub = compute_pb2_grpc.ComputeStub(ch)
        for v in vms:
            infos.append({
                'status': stub.getStatus(compute_pb2.StatusRequest(uuid=v.uuid)).message,
                'ip': stub.getIP(compute_pb2.IPRequest(uuid=v.uuid)).message
            })
    if request.method == "POST":
        uuid = request.form.get("uuid")
        action = request.form.get("action")
        if action == "start":
            with grpc.insecure_channel('localhost:8080') as ch:
                stub = compute_pb2_grpc.ComputeStub(ch)
                reply = stub.startVM(compute_pb2.StartRequest(uuid=uuid))
            print("Reply: %s" % reply.message)
        elif action == "shutdown":
            with grpc.insecure_channel('localhost:8080') as ch:
                stub = compute_pb2_grpc.ComputeStub(ch)
                reply = stub.shutdownVM(compute_pb2.ShutdownRequest(uuid=uuid))
            print("Reply: %s" % reply.message)
        elif action == "destroy":
            with grpc.insecure_channel('localhost:8080') as ch:
                stub = compute_pb2_grpc.ComputeStub(ch)
                reply = stub.destroyVM(compute_pb2.DestroyRequest(uuid=uuid))
            print("Reply: %s" % reply.message)
        elif action == "create":
            return redirect(url_for("compute.create"))
        elif action == "delete":
            with grpc.insecure_channel('localhost:8080') as ch:
                stub = compute_pb2_grpc.ComputeStub(ch)
                reply = stub.deleteVM(compute_pb2.DeleteRequest(uuid=uuid))
            print("Reply: %s" % reply.message)
            vm = VirtualMachines.query.filter_by(uuid=uuid).first()
            db.session.delete(vm)
            db.session.commit()
        else:
            print(request.form.get("action"))
    return render_template("compute/index.html", form=form, vms=vms, infos=infos, zip=zip)

@compute.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = ComputeForm()
    form.resource_group_uuid.choices = [
        (rg.uuid, rg.name) for rg in ResourceGroups.query.filter(ResourceGroups.user_id==current_user.id)
    ]
    form.network_uuid.choices = [
        (nw.uuid, nw.name) for nw in Networks.query.join(ResourceGroups).filter(ResourceGroups.user_id==current_user.id)
    ]
    form.image_id.choices = [
        (img.id, img.name) for img in Images.query.all()
    ]
    form.type_id.choices = [
        (mt.id, mt.name) for mt in MachineTypes.query.all()
    ]
    form.keypair.choices = [
        (kp.uuid, kp.name) for kp in KeyPairs.query.join(ResourceGroups).filter(ResourceGroups.user_id==current_user.id)
    ]
    if form.validate_on_submit():
        # 仮想マシン用のストレージプール作成
        pool = StoragePools(
            uuid=uuid.uuid4(),
            resource_group_uuid=form.resource_group_uuid.data,
            name=form.name.data + "StgPool",
            capacity=10
        )
        # wataame-storageにストレージプール作成を依頼
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

        # 仮想マシンインストール用のボリューム作成
        # TODO:typeによってcapacityを変更
        volume = Volumes(
            uuid=uuid.uuid4(),
            storage_pool_uuid=pool.uuid,
            name=form.name.data + "Vol",
            capacity=10,
            path=None
        )
        # wataame-storageにボリューム作成を依頼
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

        # 仮想マシンの作成
        vm = VirtualMachines(
            uuid=uuid.uuid4(),
            resource_group_uuid=form.resource_group_uuid.data,
            name=form.name.data,
            image_id=form.image_id.data,
            type_id=form.type_id.data,
            keypair_uuid=form.keypair.data,
            volume_uuid=volume.uuid,
            mac="52:54:00:%02x:%02x:%02x" % (
                random.randint(0,255),
                random.randint(0,255),
                random.randint(0,255)),
            network_uuid=form.network_uuid.data,
        )
        # wataame-computeに仮想マシン作成を依頼
        with grpc.insecure_channel('localhost:8080') as ch:
            stub = compute_pb2_grpc.ComputeStub(ch)
            network = Networks.query.filter(Networks.uuid==vm.network_uuid).first()
            keypair = KeyPairs.query.filter(KeyPairs.uuid==vm.keypair_uuid).first()
            vol = Volumes.query.filter(Volumes.uuid==vm.volume_uuid).first()
            # パスワードはSHA256でハッシュ値にする
            reply = stub.createVM(compute_pb2.CreateRequest(
                name=vm.name,
                uuid=str(vm.uuid),
                network=network.name,
                mac=vm.mac,
                hostname=str(form.hostname.data),
                password_hash=crypt.crypt(form.password.data,salt=crypt.mksalt()),
                username=form.username.data,
                pubkey=keypair.pubkey,
                imgpath=vol.path))
        print("Reply: %s" % reply.message)
        db.session.add(vm)
        db.session.commit()
        return redirect(url_for("compute.index"))
    return render_template("compute/create.html", form=form)