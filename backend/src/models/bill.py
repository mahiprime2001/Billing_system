from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Bill(db.Model):
    __tablename__ = 'bills'
    
    id = db.Column(db.Integer, primary_key=True)
    bill_number = db.Column(db.String(20), unique=True, nullable=False)
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchants.id', ondelete='CASCADE'), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('store_locations.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    bill_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    tax_amount = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    discount_amount = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    status = db.Column(db.String(20), nullable=False, default='pending')  # 'pending', 'paid', 'partially_paid', 'overdue', 'cancelled'
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = db.relationship('BillItem', backref='bill', lazy=True, cascade="all, delete-orphan")
    payments = db.relationship('Payment', backref='bill', lazy=True, cascade="all, delete-orphan")
    temporary_links = db.relationship('TemporaryLink', 
                                     primaryjoin="and_(Bill.id==TemporaryLink.related_entity_id, "
                                                "TemporaryLink.related_entity_type=='bill')",
                                     backref='bill', lazy=True)
    
    def __repr__(self):
        return f'<Bill {self.bill_number}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'bill_number': self.bill_number,
            'merchant_id': self.merchant_id,
            'store_id': self.store_id,
            'user_id': self.user_id,
            'bill_date': self.bill_date.isoformat() if self.bill_date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'total_amount': float(self.total_amount),
            'tax_amount': float(self.tax_amount),
            'discount_amount': float(self.discount_amount),
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class BillItem(db.Model):
    __tablename__ = 'bill_items'
    
    id = db.Column(db.Integer, primary_key=True)
    bill_id = db.Column(db.Integer, db.ForeignKey('bills.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    product_name = db.Column(db.String(100), nullable=False)  # Stored separately in case product details change
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    tax_rate = db.Column(db.Numeric(5, 2), nullable=False, default=0)
    tax_amount = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    discount_amount = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<BillItem {self.id} for bill {self.bill_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'bill_id': self.bill_id,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'quantity': self.quantity,
            'unit_price': float(self.unit_price),
            'tax_rate': float(self.tax_rate),
            'tax_amount': float(self.tax_amount),
            'discount_amount': float(self.discount_amount),
            'total_amount': float(self.total_amount),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    bill_id = db.Column(db.Integer, db.ForeignKey('bills.id', ondelete='CASCADE'), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)  # 'cash', 'upi', 'card', etc.
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    transaction_reference = db.Column(db.String(100))
    status = db.Column(db.String(20), nullable=False, default='completed')  # 'completed', 'pending', 'failed', 'refunded'
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_by = db.Column(db.Integer)  # User or merchant who recorded the payment
    
    def __repr__(self):
        return f'<Payment {self.id} for bill {self.bill_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'bill_id': self.bill_id,
            'payment_method': self.payment_method,
            'amount': float(self.amount),
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'transaction_reference': self.transaction_reference,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_by': self.updated_by
        }
