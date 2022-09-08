from datetime import datetime

from apps.main import db

class ResourceGroups(db.Model):
    __tablename__ = "resource_groups"
    uuid = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    name = db.Column(db.String(32))
    created_at = db.Column(db.DateTime, default=datetime.now)