from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ShoppingList(db.Model):
    __tablename__ = 'shopping_lists'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = db.relationship('ShoppingListItem', backref='shopping_list', lazy=True, cascade="all, delete-orphan")
    shared_with = db.relationship('ListSharing', 
                                 foreign_keys='ListSharing.list_id',
                                 backref='shared_list', 
                                 lazy=True, 
                                 cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<ShoppingList {self.name} for user {self.user_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class ShoppingListItem(db.Model):
    __tablename__ = 'shopping_list_items'
    
    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('shopping_lists.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    custom_item_name = db.Column(db.String(100))  # For items not in the product database
    quantity = db.Column(db.Integer, nullable=False, default=1)
    is_purchased = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        item_name = self.custom_item_name if self.custom_item_name else f"product_id: {self.product_id}"
        return f'<ShoppingListItem {item_name} for list {self.list_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'list_id': self.list_id,
            'product_id': self.product_id,
            'custom_item_name': self.custom_item_name,
            'quantity': self.quantity,
            'is_purchased': self.is_purchased,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class ListSharing(db.Model):
    __tablename__ = 'list_sharing'
    
    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('shopping_lists.id', ondelete='CASCADE'), nullable=False)
    shared_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    shared_with = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    shared_at = db.Column(db.DateTime, default=datetime.utcnow)
    access_level = db.Column(db.String(20), default='view')  # 'view', 'edit'
    status = db.Column(db.String(20), default='pending')  # 'pending', 'accepted', 'declined'
    last_accessed = db.Column(db.DateTime)
    
    __table_args__ = (
        db.UniqueConstraint('list_id', 'shared_with', name='uix_list_shared_with'),
    )
    
    # Relationships
    shared_by_user = db.relationship('User', foreign_keys=[shared_by], backref='shared_lists')
    shared_with_user = db.relationship('User', foreign_keys=[shared_with], backref='received_shared_lists')
    
    def __repr__(self):
        return f'<ListSharing list {self.list_id} shared by {self.shared_by} with {self.shared_with}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'list_id': self.list_id,
            'shared_by': self.shared_by,
            'shared_with': self.shared_with,
            'shared_at': self.shared_at.isoformat() if self.shared_at else None,
            'access_level': self.access_level,
            'status': self.status,
            'last_accessed': self.last_accessed.isoformat() if self.last_accessed else None
        }
