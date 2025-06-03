from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    profile_image_url = db.Column(db.String(255))
    preferred_payment_method = db.Column(db.String(50))
    default_address_id = db.Column(db.Integer)
    
    # Relationships
    addresses = db.relationship('UserAddress', backref='user', lazy=True, cascade="all, delete-orphan")
    authentication_methods = db.relationship('UserAuthentication', backref='user', lazy=True, cascade="all, delete-orphan")
    shopping_lists = db.relationship('ShoppingList', backref='user', lazy=True, cascade="all, delete-orphan")
    bills = db.relationship('Bill', backref='user', lazy=True)
    pickup_requests = db.relationship('PickupRequest', backref='user', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)
    sessions = db.relationship('Session', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'phone_number': self.phone_number,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active,
            'profile_image_url': self.profile_image_url,
            'preferred_payment_method': self.preferred_payment_method
        }


class UserAuthentication(db.Model):
    __tablename__ = 'user_authentication'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    auth_type = db.Column(db.String(20), nullable=False)  # 'password', 'google_auth', 'microsoft_auth', etc.
    auth_key = db.Column(db.String(255))  # For storing authenticator app keys
    is_primary = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_used = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<UserAuthentication {self.auth_type} for user {self.user_id}>'


class UserAddress(db.Model):
    __tablename__ = 'user_addresses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    address_line1 = db.Column(db.String(100), nullable=False)
    address_line2 = db.Column(db.String(100))
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(50), nullable=False, default='India')
    is_default = db.Column(db.Boolean, default=False)
    label = db.Column(db.String(50))  # 'home', 'work', etc.
    location = db.Column(db.String(100))  # Will be replaced with PostGIS GEOGRAPHY(POINT) in production
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<UserAddress {self.id} for user {self.user_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'address_line1': self.address_line1,
            'address_line2': self.address_line2,
            'city': self.city,
            'state': self.state,
            'postal_code': self.postal_code,
            'country': self.country,
            'is_default': self.is_default,
            'label': self.label,
            'location': self.location
        }
