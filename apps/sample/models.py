"""
from datetime import datetime
from apps.main import db

class Samples(db.Model):
    __tablename__ = "samples"
    uuid = db.Column(db.String(36), primary_key=True)
    resource_group_uuid = db.Column(db.String(36), db.ForeignKey("resource_groups.uuid"))
    name = db.Column(db.String(32))
    created_at = db.Column(db.DateTime, default=datetime.now)
"""