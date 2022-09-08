from datetime import datetime

from apps.main import db

class Containers(db.Model):
    __tablename__ = "containers"
    id = db.Column(db.String(64), primary_key=True)
    resource_group_uuid = db.Column(db.String(36), db.ForeignKey("resource_groups.uuid"))
    network_uuid = db.Column(db.String(36), db.ForeignKey("networks.uuid"))
    name = db.Column(db.String(32))
    image = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.now)