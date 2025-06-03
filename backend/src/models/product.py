from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'))
    base_price = db.Column(db.Numeric(10, 2), nullable=False)
    tax_rate = db.Column(db.Numeric(5, 2), default=0)
    sku = db.Column(db.String(50))
    barcode = db.Column(db.String(50))
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    category = db.relationship('ProductCategory', backref='products')
    inventory_items = db.relationship('MerchantInventory', backref='product', lazy=True)
    bill_items = db.relationship('BillItem', backref='product', lazy=True)
    shopping_list_items = db.relationship('ShoppingListItem', backref='product', lazy=True)
    pickup_request_items = db.relationship('PickupRequestItem', backref='product', lazy=True)
    
    def __repr__(self):
        return f'<Product {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category_id': self.category_id,
            'base_price': float(self.base_price),
            'tax_rate': float(self.tax_rate),
            'sku': self.sku,
            'barcode': self.barcode,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class ProductCategory(db.Model):
    __tablename__ = 'product_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    parent_category_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    subcategories = db.relationship('ProductCategory', backref=db.backref('parent_category', remote_side=[id]))
    
    def __repr__(self):
        return f'<ProductCategory {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'parent_category_id': self.parent_category_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class MerchantInventory(db.Model):
    __tablename__ = 'merchant_inventory'
    
    id = db.Column(db.Integer, primary_key=True)
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchants.id', ondelete='CASCADE'), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('store_locations.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    last_restocked = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('merchant_id', 'store_id', 'product_id', name='uix_merchant_store_product'),
    )
    
    def __repr__(self):
        return f'<MerchantInventory for merchant {self.merchant_id}, product {self.product_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'merchant_id': self.merchant_id,
            'store_id': self.store_id,
            'product_id': self.product_id,
            'stock_quantity': self.stock_quantity,
            'price': float(self.price),
            'is_available': self.is_available,
            'last_restocked': self.last_restocked.isoformat() if self.last_restocked else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
