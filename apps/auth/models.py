from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from apps.main import db, login_manager

class Users(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256))
    email = db.Column(db.String(256), unique=True)
    password_hash = db.Column(db.String(256))
    created_at = db.Column(
        db.DateTime, 
        default=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    updated_at = db.Column(
        db.DateTime,
        default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        onupdate=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    @property
    def password(self):
        raise AttributeError("Can't read")
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)
