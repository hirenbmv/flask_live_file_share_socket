from app import db
from datetime import datetime

class Room(db.Model):

    __tablename__ = "room"

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer,unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    # updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)