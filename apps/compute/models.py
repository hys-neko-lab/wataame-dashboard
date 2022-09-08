from datetime import datetime

from apps.main import db

class VirtualMachines(db.Model):
    __tablename__ = "virtual_machines"
    uuid = db.Column(db.String(36), primary_key=True)
    resource_group_uuid = db.Column(db.String(36), db.ForeignKey("resource_groups.uuid"))
    name = db.Column(db.String(32))
    image_id = db.Column(db.Integer, db.ForeignKey("images.id"))
    type_id = db.Column(db.Integer, db.ForeignKey("machine_types.id"))
    keypair_uuid=db.Column(db.String(36), db.ForeignKey("keypairs.uuid"))
    volume_uuid = db.Column(db.String(36), db.ForeignKey("volumes.uuid"))
    mac=db.Column(db.String(17))
    network_uuid = db.Column(db.String(36), db.ForeignKey("networks.uuid"))
    created_at = db.Column(db.DateTime, default=datetime.now)

class Images(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    path = db.Column(db.String(256))

class MachineTypes(db.Model):
    __tablename__ = "machine_types"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
