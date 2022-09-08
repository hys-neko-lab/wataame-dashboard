from datetime import datetime

from apps.main import db

class StoragePools(db.Model):
    __tablename__ = "storage_pools"
    uuid = db.Column(db.String(36), primary_key=True)
    resource_group_uuid = db.Column(db.String(36), db.ForeignKey("resource_groups.uuid"))
    name = db.Column(db.String(32))
    capacity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now)

class Volumes(db.Model):
    __tablename__ = "volumes"
    uuid = db.Column(db.String(36), primary_key=True)
    storage_pool_uuid = db.Column(db.String(36), db.ForeignKey("storage_pools.uuid"))
    name = db.Column(db.String(32))
    capacity = db.Column(db.Integer)
    path = db.Column(db.String(512))
    created_at = db.Column(db.DateTime, default=datetime.now)