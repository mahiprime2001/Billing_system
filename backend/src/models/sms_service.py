from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import jwt
import os
import secrets
import string

db = SQLAlchemy()

class SMSService:
    """Service for handling SMS notifications with temporary links."""
    
    SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'development_secret_key')
    BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5000')
    
    @classmethod
    def generate_temporary_link(cls, bill_id, user_id):
        """
        Generate a temporary link for a bill that expires after 48 hours.
        
        Args:
            bill_id: ID of the bill
            user_id: ID of the user who will receive the link
            
        Returns:
            dict: Contains the generated link and token
        """
        # Create expiration time (48 hours from now)
        expiration_time = datetime.utcnow() + timedelta(hours=48)
        
        # Create payload with bill ID, user ID and expiration time
        payload = {
            'bill_id': bill_id,
            'user_id': user_id,
            'exp': expiration_time.timestamp()
        }
        
        # Generate JWT token
        token = jwt.encode(payload, cls.SECRET_KEY, algorithm='HS256')
        
        # Create link with token
        link = f"{cls.BASE_URL}/bills/view/{token}"
        
        # Create and store temporary link in database
        temp_link = TemporaryLink(
            token=token,
            user_id=user_id,
            related_entity_type='bill',
            related_entity_id=bill_id,
            expires_at=expiration_time
        )
        
        db.session.add(temp_link)
        db.session.commit()
        
        return {
            'link': link,
            'token': token,
            'expires_at': expiration_time
        }
    
    @classmethod
    def validate_temporary_link(cls, token):
        """
        Validate a temporary link token.
        
        Args:
            token: JWT token from the link
            
        Returns:
            dict: Validation result with bill information if valid
        """
        try:
            # First check if token exists in database
            temp_link = TemporaryLink.query.filter_by(token=token).first()
            
            if not temp_link:
                return {
                    'valid': False,
                    'reason': 'invalid',
                    'redirect_to': '/invalid-link'
                }
            
            # Check if link is revoked or expired in database
            if temp_link.is_revoked:
                return {
                    'valid': False,
                    'reason': 'revoked',
                    'redirect_to': '/expired-link'
                }
            
            now = datetime.utcnow()
            if now > temp_link.expires_at:
                return {
                    'valid': False,
                    'reason': 'expired',
                    'redirect_to': '/expired-link'
                }
            
            # Decode and validate token
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=['HS256'])
            
            # Record access
            temp_link.record_access()
            db.session.commit()
            
            # Token is valid, return bill information
            bill_id = payload['bill_id']
            user_id = payload['user_id']
            
            return {
                'valid': True,
                'bill_id': bill_id,
                'user_id': user_id
            }
            
        except jwt.ExpiredSignatureError:
            return {
                'valid': False,
                'reason': 'expired',
                'redirect_to': '/expired-link'
            }
        except (jwt.InvalidTokenError, Exception) as e:
            return {
                'valid': False,
                'reason': 'invalid',
                'redirect_to': '/invalid-link'
            }
    
    @classmethod
    def send_bill_notification(cls, bill, user):
        """
        Send SMS notification for a bill with a temporary link.
        
        Args:
            bill: Bill object
            user: User object
            
        Returns:
            dict: Result of the SMS sending operation
        """
        # Generate temporary link
        link_data = cls.generate_temporary_link(bill.id, user.id)
        
        # Create message with temporary link
        message = (
            f"You have a new bill #{bill.bill_number} from {bill.merchant.business_name} "
            f"for Rs. {bill.total_amount}. View your bill (valid for 48 hours): {link_data['link']}"
        )
        
        # Create SMS notification record
        sms = SMSNotification(
            phone_number=user.phone_number,
            message=message,
            temporary_link=link_data['link'],
            link_expiry=link_data['expires_at'],
            related_entity_type='bill',
            related_entity_id=bill.id
        )
        
        db.session.add(sms)
        db.session.commit()
        
        # In a real implementation, this would call an SMS gateway API
        # For now, we'll just simulate it
        sms.status = 'sent'
        sms.sent_at = datetime.utcnow()
        db.session.commit()
        
        # Create in-app notification as well
        notification = Notification(
            user_id=user.id,
            type='bill',
            title=f"New Bill #{bill.bill_number}",
            message=f"You have received a new bill from {bill.merchant.business_name} for Rs. {bill.total_amount}.",
            related_entity_type='bill',
            related_entity_id=bill.id
        )
        
        db.session.add(notification)
        db.session.commit()
        
        return {
            'success': True,
            'sms_id': sms.id,
            'notification_id': notification.id,
            'message': message
        }
    
    @classmethod
    def handle_expired_link(cls):
        """
        Generate response for expired link.
        
        Returns:
            dict: Response data for expired link page
        """
        return {
            'message': 'This link has expired. Bills are available for 48 hours via SMS links.',
            'options': [
                {
                    'text': 'Download our app',
                    'link': '/download-app'
                },
                {
                    'text': 'Log in to view all bills',
                    'link': '/login'
                }
            ]
        }
