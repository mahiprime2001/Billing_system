from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

db = SQLAlchemy()

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchants.id', ondelete='CASCADE'))
    type = db.Column(db.String(50), nullable=False)  # 'bill', 'payment', 'pickup', etc.
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    related_entity_type = db.Column(db.String(50))  # 'bill', 'payment', 'pickup', etc.
    related_entity_id = db.Column(db.Integer)  # ID of the related entity
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        recipient = f"user {self.user_id}" if self.user_id else f"merchant {self.merchant_id}"
        return f'<Notification {self.id} for {recipient}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'merchant_id': self.merchant_id,
            'type': self.type,
            'title': self.title,
            'message': self.message,
            'is_read': self.is_read,
            'related_entity_type': self.related_entity_type,
            'related_entity_id': self.related_entity_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class SMSNotification(db.Model):
    __tablename__ = 'sms_notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(15), nullable=False)
    message = db.Column(db.Text, nullable=False)
    temporary_link = db.Column(db.String(255))
    link_expiry = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'sent', 'delivered', 'failed'
    related_entity_type = db.Column(db.String(50))  # 'bill', 'payment', 'pickup', etc.
    related_entity_id = db.Column(db.Integer)  # ID of the related entity
    sent_at = db.Column(db.DateTime)
    delivery_status_updated_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<SMSNotification {self.id} to {self.phone_number}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'phone_number': self.phone_number,
            'message': self.message,
            'temporary_link': self.temporary_link,
            'link_expiry': self.link_expiry.isoformat() if self.link_expiry else None,
            'status': self.status,
            'related_entity_type': self.related_entity_type,
            'related_entity_id': self.related_entity_id,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'delivery_status_updated_at': self.delivery_status_updated_at.isoformat() if self.delivery_status_updated_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class TemporaryLink(db.Model):
    __tablename__ = 'temporary_links'
    
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    related_entity_type = db.Column(db.String(50), nullable=False)  # 'bill', 'payment', etc.
    related_entity_id = db.Column(db.Integer, nullable=False)  # ID of the related entity
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)  # 48 hours after creation
    is_accessed = db.Column(db.Boolean, default=False)
    first_accessed_at = db.Column(db.DateTime)
    access_count = db.Column(db.Integer, default=0)
    last_accessed_at = db.Column(db.DateTime)
    is_revoked = db.Column(db.Boolean, default=False)
    revoked_at = db.Column(db.DateTime)
    
    # Relationships
    user = db.relationship('User', backref='temporary_links')
    
    def __repr__(self):
        return f'<TemporaryLink {self.token[:8]}... for {self.related_entity_type} {self.related_entity_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'token': self.token,
            'user_id': self.user_id,
            'related_entity_type': self.related_entity_type,
            'related_entity_id': self.related_entity_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'is_accessed': self.is_accessed,
            'first_accessed_at': self.first_accessed_at.isoformat() if self.first_accessed_at else None,
            'access_count': self.access_count,
            'last_accessed_at': self.last_accessed_at.isoformat() if self.last_accessed_at else None,
            'is_revoked': self.is_revoked,
            'revoked_at': self.revoked_at.isoformat() if self.revoked_at else None
        }
    
    @classmethod
    def create_for_entity(cls, user_id, entity_type, entity_id):
        """Create a temporary link for an entity with 48-hour expiry."""
        import secrets
        import string
        
        # Generate a secure random token
        token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(64))
        
        # Set expiry to 48 hours from now
        expires_at = datetime.utcnow() + timedelta(hours=48)
        
        # Create and return the temporary link
        temp_link = cls(
            token=token,
            user_id=user_id,
            related_entity_type=entity_type,
            related_entity_id=entity_id,
            expires_at=expires_at
        )
        
        return temp_link
    
    def is_valid(self):
        """Check if the temporary link is valid."""
        now = datetime.utcnow()
        return (not self.is_revoked and 
                now < self.expires_at)
    
    def record_access(self):
        """Record an access to this temporary link."""
        now = datetime.utcnow()
        
        if not self.is_accessed:
            self.is_accessed = True
            self.first_accessed_at = now
        
        self.access_count += 1
        self.last_accessed_at = now
        
        return True
    
    def revoke(self):
        """Revoke this temporary link."""
        self.is_revoked = True
        self.revoked_at = datetime.utcnow()
        
        return True
