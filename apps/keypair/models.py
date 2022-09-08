from datetime import datetime

from apps.main import db

class KeyPairs(db.Model):
    __tablename__ = "keypairs"
    uuid = db.Column(db.String(36), primary_key=True)
    resource_group_uuid = db.Column(db.String(36), db.ForeignKey("resource_groups.uuid"))
    name = db.Column(db.String(32))
    pubkey = db.Column(db.String(1024))
    created_at = db.Column(db.DateTime, default=datetime.now)