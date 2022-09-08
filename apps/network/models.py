from datetime import datetime

from apps.main import db

class Networks(db.Model):
    __tablename__ = "networks"
    uuid = db.Column(db.String(36), primary_key=True)
    docknetid = db.Column(db.String(64))
    resource_group_uuid = db.Column(db.String(36), db.ForeignKey("resource_groups.uuid"))
    name = db.Column(db.String(32))
    type = db.Column(db.String(16))
    cidr=db.Column(db.String(18))
    mac=db.Column(db.String(17))
    created_at = db.Column(db.DateTime, default=datetime.now)