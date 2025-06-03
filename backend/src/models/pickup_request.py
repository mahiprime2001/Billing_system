from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

db = SQLAlchemy()

class PickupRequest(db.Model):
    __tablename__ = 'pickup_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchants.id', ondelete='CASCADE'), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('store_locations.id'))
    status = db.Column(db.String(20), nullable=False, default='pending')  # 'pending', 'accepted', 'ready', 'completed', 'cancelled'
    requested_pickup_time = db.Column(db.DateTime)
    actual_pickup_time = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = db.relationship('PickupRequestItem', backref='pickup_request', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<PickupRequest {self.id} by user {self.user_id} from merchant {self.merchant_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'merchant_id': self.merchant_id,
            'store_id': self.store_id,
            'status': self.status,
            'requested_pickup_time': self.requested_pickup_time.isoformat() if self.requested_pickup_time else None,
            'actual_pickup_time': self.actual_pickup_time.isoformat() if self.actual_pickup_time else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class PickupRequestItem(db.Model):
    __tablename__ = 'pickup_request_items'
    
    id = db.Column(db.Integer, primary_key=True)
    pickup_request_id = db.Column(db.Integer, db.ForeignKey('pickup_requests.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    custom_item_name = db.Column(db.String(100))  # For items not in the product database
    quantity = db.Column(db.Integer, nullable=False, default=1)
    status = db.Column(db.String(20), nullable=False, default='pending')  # 'pending', 'available', 'unavailable', 'substituted'
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        item_name = self.custom_item_name if self.custom_item_name else f"product_id: {self.product_id}"
        return f'<PickupRequestItem {item_name} for request {self.pickup_request_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'pickup_request_id': self.pickup_request_id,
            'product_id': self.product_id,
            'custom_item_name': self.custom_item_name,
            'quantity': self.quantity,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
