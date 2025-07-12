from app import db
from datetime import datetime

class Gear(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # hookah, bowl, hose, hmd, etc.
    brand = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100))
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    image_url = db.Column(db.String(500))
    product_url = db.Column(db.String(500))
    specifications = db.Column(db.JSON)  # Store specs as JSON
    compatibility_tags = db.Column(db.JSON)  # Store compatibility info as JSON
    rating = db.Column(db.Float, default=0.0)
    review_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'brand': self.brand,
            'model': self.model,
            'description': self.description,
            'price': self.price,
            'image_url': self.image_url,
            'product_url': self.product_url,
            'specifications': self.specifications or {},
            'compatibility_tags': self.compatibility_tags or [],
            'rating': self.rating,
            'review_count': self.review_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<Gear {self.brand} {self.name}>' 