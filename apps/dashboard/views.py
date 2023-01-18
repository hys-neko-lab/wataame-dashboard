from flask import Blueprint, render_template
from flask_login import login_required, current_user

from apps.resource.models import ResourceGroups
from apps.keypair.models import KeyPairs
from apps.compute.models import VirtualMachines
from apps.network.models import Networks
from apps.storage.models import StoragePools, Volumes
from apps.container.models import Containers
from apps.serverless.models import Serverlesses

dashboard = Blueprint(
    "dashboard",
    __name__,
    template_folder="templates",
    static_folder = "static"
)

@dashboard.route("/")
@login_required
def index():
    # 各種リソースのサマリーを取得
    # Resource
    resource_groups = ResourceGroups.query.filter(ResourceGroups.user_id==current_user.id)
    rg = get_summary(resource_groups, ResourceGroups)
    # Keypair
    keypairs = KeyPairs.query.join(ResourceGroups).filter(ResourceGroups.user_id==current_user.id)
    keypair = get_summary(keypairs, KeyPairs)
    # Compute
    vms = VirtualMachines.query.join(ResourceGroups).filter(ResourceGroups.user_id==current_user.id)
    vm = get_summary(vms, VirtualMachines)
    # Network
    networks = Networks.query.join(ResourceGroups).filter(ResourceGroups.user_id==current_user.id)
    network = get_summary(networks, Networks)
    # Storage
    pools = StoragePools.query.join(ResourceGroups).filter(ResourceGroups.user_id==current_user.id)
    volumes = Volumes.query.join(pools)
    volume = get_summary(volumes, Volumes)
    # Container
    containers = Containers.query.join(ResourceGroups).filter(ResourceGroups.user_id==current_user.id)
    container = get_summary(containers, Containers)
    # Serverless
    serverlesses = Serverlesses.query.join(ResourceGroups).filter(ResourceGroups.user_id==current_user.id)
    serverless = get_summary(serverlesses, Serverlesses)

    return render_template("index.html",
        rg=rg,
        keypair=keypair,
        vm=vm,
        network=network,
        volume=volume,
        container=container,
        serverless=serverless)

def get_summary(resources, Model):
    # リソースの数と最新の作成日時をデータベースから取得
    try:
        resource = {"num": resources.count(), "created_at": resources.order_by(Model.created_at.desc()).first().created_at}
    except:
        resource = {"num": 0, "created_at": "None"}
    return resource