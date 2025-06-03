from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Merchant(db.Model):
    __tablename__ = 'merchants'
    
    id = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String(100), nullable=False)
    gst_number = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    contact_person = db.Column(db.String(100))
    business_type = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    logo_url = db.Column(db.String(255))
    website_url = db.Column(db.String(255))
    
    # Relationships
    authentication_methods = db.relationship('MerchantAuthentication', backref='merchant', lazy=True, cascade="all, delete-orphan")
    store_locations = db.relationship('StoreLocation', backref='merchant', lazy=True, cascade="all, delete-orphan")
    inventory_items = db.relationship('MerchantInventory', backref='merchant', lazy=True, cascade="all, delete-orphan")
    bills = db.relationship('Bill', backref='merchant', lazy=True)
    pickup_requests = db.relationship('PickupRequest', backref='merchant', lazy=True)
    notifications = db.relationship('Notification', backref='merchant', lazy=True)
    sessions = db.relationship('Session', backref='merchant', lazy=True)
    
    def __repr__(self):
        return f'<Merchant {self.business_name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'business_name': self.business_name,
            'gst_number': self.gst_number,
            'email': self.email,
            'phone_number': self.phone_number,
            'contact_person': self.contact_person,
            'business_type': self.business_type,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'logo_url': self.logo_url,
            'website_url': self.website_url
        }


class MerchantAuthentication(db.Model):
    __tablename__ = 'merchant_authentication'
    
    id = db.Column(db.Integer, primary_key=True)
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchants.id', ondelete='CASCADE'), nullable=False)
    auth_type = db.Column(db.String(20), nullable=False)  # 'password', 'google_auth', 'microsoft_auth', etc.
    auth_key = db.Column(db.String(255))  # For storing authenticator app keys
    is_primary = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_used = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<MerchantAuthentication {self.auth_type} for merchant {self.merchant_id}>'


class StoreLocation(db.Model):
    __tablename__ = 'store_locations'
    
    id = db.Column(db.Integer, primary_key=True)
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchants.id', ondelete='CASCADE'), nullable=False)
    store_name = db.Column(db.String(100), nullable=False)
    address_line1 = db.Column(db.String(100), nullable=False)
    address_line2 = db.Column(db.String(100))
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(50), nullable=False, default='India')
    location = db.Column(db.String(100), nullable=False)  # Will be replaced with PostGIS GEOGRAPHY(POINT) in production
    contact_number = db.Column(db.String(15))
    opening_time = db.Column(db.Time)
    closing_time = db.Column(db.Time)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    operating_hours = db.relationship('StoreOperatingHours', backref='store', lazy=True, cascade="all, delete-orphan")
    inventory_items = db.relationship('MerchantInventory', backref='store', lazy=True)
    bills = db.relationship('Bill', backref='store', lazy=True)
    pickup_requests = db.relationship('PickupRequest', backref='store', lazy=True)
    
    def __repr__(self):
        return f'<StoreLocation {self.store_name} for merchant {self.merchant_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'merchant_id': self.merchant_id,
            'store_name': self.store_name,
            'address_line1': self.address_line1,
            'address_line2': self.address_line2,
            'city': self.city,
            'state': self.state,
            'postal_code': self.postal_code,
            'country': self.country,
            'location': self.location,
            'contact_number': self.contact_number,
            'opening_time': self.opening_time.isoformat() if self.opening_time else None,
            'closing_time': self.closing_time.isoformat() if self.closing_time else None,
            'is_active': self.is_active
        }


class StoreOperatingHours(db.Model):
    __tablename__ = 'store_operating_hours'
    
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('store_locations.id', ondelete='CASCADE'), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)  # 0 = Sunday, 1 = Monday, etc.
    opening_time = db.Column(db.Time, nullable=False)
    closing_time = db.Column(db.Time, nullable=False)
    is_closed = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<StoreOperatingHours for store {self.store_id} on day {self.day_of_week}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'store_id': self.store_id,
            'day_of_week': self.day_of_week,
            'opening_time': self.opening_time.isoformat() if self.opening_time else None,
            'closing_time': self.closing_time.isoformat() if self.closing_time else None,
            'is_closed': self.is_closed
        }
