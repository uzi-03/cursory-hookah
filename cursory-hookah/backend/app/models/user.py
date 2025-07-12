from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # User's gear collection (many-to-many relationship)
    owned_gear = db.relationship('UserGear', backref='user', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class UserGear(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    gear_id = db.Column(db.Integer, db.ForeignKey('gear.id'), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to Gear
    gear = db.relationship('Gear', backref='user_gear')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'gear_id': self.gear_id,
            'gear': self.gear.to_dict() if self.gear else None,
            'added_at': self.added_at.isoformat() if self.added_at else None
        } 