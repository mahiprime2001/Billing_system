from flask import Blueprint, request, jsonify
from src.models.sms_service import SMSService
from src.models.bill import Bill
from src.models.user import User
from src.models.merchant import Merchant
from src.models.notification import TemporaryLink
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
sms_bp = Blueprint('sms', __name__)

@sms_bp.route('/send-bill-notification', methods=['POST'])
def send_bill_notification():
    """
    Send SMS notification for a bill with a temporary link.
    
    Request body:
    {
        "bill_id": 123,
        "user_id": 456
    }
    """
    data = request.json
    
    if not data or 'bill_id' not in data or 'user_id' not in data:
        return jsonify({
            'success': False,
            'message': 'Missing required fields: bill_id, user_id'
        }), 400
    
    bill_id = data['bill_id']
    user_id = data['user_id']
    
    # Get bill and user
    bill = Bill.query.get(bill_id)
    user = User.query.get(user_id)
    
    if not bill:
        return jsonify({
            'success': False,
            'message': f'Bill with ID {bill_id} not found'
        }), 404
    
    if not user:
        return jsonify({
            'success': False,
            'message': f'User with ID {user_id} not found'
        }), 404
    
    # Check if bill belongs to user
    if bill.user_id != user_id:
        return jsonify({
            'success': False,
            'message': 'Bill does not belong to this user'
        }), 403
    
    # Send notification
    result = SMSService.send_bill_notification(bill, user)
    
    return jsonify(result), 200

@sms_bp.route('/validate-link/<token>', methods=['GET'])
def validate_link(token):
    """
    Validate a temporary link token.
    """
    result = SMSService.validate_temporary_link(token)
    
    if result['valid']:
        # If valid, redirect to bill view
        bill_id = result['bill_id']
        return jsonify({
            'success': True,
            'redirect_to': f'/bills/{bill_id}'
        }), 200
    else:
        # If invalid, return error
        return jsonify({
            'success': False,
            'reason': result['reason'],
            'redirect_to': result['redirect_to']
        }), 400

@sms_bp.route('/expired-link', methods=['GET'])
def expired_link():
    """
    Handle expired link page.
    """
    response = SMSService.handle_expired_link()
    return jsonify(response), 200

@sms_bp.route('/revoke-link/<token>', methods=['POST'])
def revoke_link(token):
    """
    Revoke a temporary link.
    """
    temp_link = TemporaryLink.query.filter_by(token=token).first()
    
    if not temp_link:
        return jsonify({
            'success': False,
            'message': 'Link not found'
        }), 404
    
    temp_link.revoke()
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Link revoked successfully'
    }), 200
