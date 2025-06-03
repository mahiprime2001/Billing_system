from flask import Blueprint, request, jsonify, render_template
from src.models.bill import Bill, BillItem, Payment
from src.models.user import User
from src.models.merchant import Merchant, StoreLocation
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
bill_bp = Blueprint('bill', __name__)

@bill_bp.route('/', methods=['GET'])
def get_bills():
    """
    Get all bills for a user.
    
    Query parameters:
    - user_id: ID of the user
    - status: Filter by status (optional)
    - from_date: Filter by date from (optional)
    - to_date: Filter by date to (optional)
    """
    user_id = request.args.get('user_id')
    status = request.args.get('status')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    
    if not user_id:
        return jsonify({
            'success': False,
            'message': 'Missing required parameter: user_id'
        }), 400
    
    # Build query
    query = Bill.query.filter_by(user_id=user_id)
    
    # Apply filters
    if status:
        query = query.filter_by(status=status)
    
    if from_date:
        try:
            from_date_obj = datetime.fromisoformat(from_date)
            query = query.filter(Bill.bill_date >= from_date_obj)
        except ValueError:
            return jsonify({
                'success': False,
                'message': 'Invalid from_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'
            }), 400
    
    if to_date:
        try:
            to_date_obj = datetime.fromisoformat(to_date)
            query = query.filter(Bill.bill_date <= to_date_obj)
        except ValueError:
            return jsonify({
                'success': False,
                'message': 'Invalid to_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'
            }), 400
    
    # Execute query
    bills = query.order_by(Bill.bill_date.desc()).all()
    
    # Format response
    result = []
    for bill in bills:
        merchant = Merchant.query.get(bill.merchant_id)
        store = StoreLocation.query.get(bill.store_id) if bill.store_id else None
        
        bill_data = bill.to_dict()
        bill_data['merchant_name'] = merchant.business_name if merchant else None
        bill_data['store_name'] = store.store_name if store else None
        
        result.append(bill_data)
    
    return jsonify({
        'success': True,
        'count': len(result),
        'bills': result
    }), 200

@bill_bp.route('/<int:bill_id>', methods=['GET'])
def get_bill(bill_id):
    """
    Get a specific bill by ID.
    """
    bill = Bill.query.get(bill_id)
    
    if not bill:
        return jsonify({
            'success': False,
            'message': f'Bill with ID {bill_id} not found'
        }), 404
    
    # Get merchant and store
    merchant = Merchant.query.get(bill.merchant_id)
    store = StoreLocation.query.get(bill.store_id) if bill.store_id else None
    
    # Get bill items
    items = BillItem.query.filter_by(bill_id=bill_id).all()
    items_data = [item.to_dict() for item in items]
    
    # Get payments
    payments = Payment.query.filter_by(bill_id=bill_id).all()
    payments_data = [payment.to_dict() for payment in payments]
    
    # Calculate payment summary
    total_paid = sum(payment.amount for payment in payments)
    remaining_amount = bill.total_amount - total_paid
    
    # Format response
    result = bill.to_dict()
    result['merchant'] = merchant.to_dict() if merchant else None
    result['store'] = store.to_dict() if store else None
    result['items'] = items_data
    result['payments'] = payments_data
    result['payment_summary'] = {
        'total_amount': float(bill.total_amount),
        'total_paid': float(total_paid),
        'remaining_amount': float(remaining_amount),
        'is_fully_paid': remaining_amount <= 0
    }
    
    return jsonify({
        'success': True,
        'bill': result
    }), 200

@bill_bp.route('/', methods=['POST'])
def create_bill():
    """
    Create a new bill.
    
    Request body:
    {
        "merchant_id": 123,
        "store_id": 456,
        "user_id": 789,
        "bill_date": "2025-06-03T12:00:00",
        "due_date": "2025-06-10T12:00:00",
        "items": [
            {
                "product_id": 1,
                "product_name": "Product 1",
                "quantity": 2,
                "unit_price": 100.00,
                "tax_rate": 18.00,
                "discount_amount": 0.00
            }
        ],
        "notes": "Optional notes"
    }
    """
    data = request.json
    
    # Validate required fields
    required_fields = ['merchant_id', 'user_id', 'items']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'success': False,
                'message': f'Missing required field: {field}'
            }), 400
    
    # Validate items
    if not data['items'] or not isinstance(data['items'], list):
        return jsonify({
            'success': False,
            'message': 'Items must be a non-empty list'
        }), 400
    
    for item in data['items']:
        required_item_fields = ['product_name', 'quantity', 'unit_price']
        for field in required_item_fields:
            if field not in item:
                return jsonify({
                    'success': False,
                    'message': f'Missing required field in item: {field}'
                }), 400
    
    # Generate bill number
    bill_number = f"BILL-{datetime.utcnow().strftime('%Y%m%d')}-{secrets.randbelow(10000):04d}"
    
    # Calculate totals
    total_amount = 0
    tax_amount = 0
    
    for item in data['items']:
        quantity = item['quantity']
        unit_price = item['unit_price']
        tax_rate = item.get('tax_rate', 0)
        discount_amount = item.get('discount_amount', 0)
        
        item_subtotal = quantity * unit_price
        item_tax = (item_subtotal * tax_rate / 100) if tax_rate else 0
        item_total = item_subtotal + item_tax - discount_amount
        
        # Add to bill totals
        total_amount += item_total
        tax_amount += item_tax
        
        # Add calculated values to item
        item['tax_amount'] = item_tax
        item['total_amount'] = item_total
    
    # Create bill
    bill = Bill(
        bill_number=bill_number,
        merchant_id=data['merchant_id'],
        store_id=data.get('store_id'),
        user_id=data['user_id'],
        bill_date=datetime.fromisoformat(data['bill_date']) if 'bill_date' in data else datetime.utcnow(),
        due_date=datetime.fromisoformat(data['due_date']) if 'due_date' in data else None,
        total_amount=total_amount,
        tax_amount=tax_amount,
        discount_amount=data.get('discount_amount', 0),
        status='pending',
        notes=data.get('notes')
    )
    
    db.session.add(bill)
    db.session.flush()  # Get bill ID without committing
    
    # Create bill items
    for item_data in data['items']:
        item = BillItem(
            bill_id=bill.id,
            product_id=item_data.get('product_id'),
            product_name=item_data['product_name'],
            quantity=item_data['quantity'],
            unit_price=item_data['unit_price'],
            tax_rate=item_data.get('tax_rate', 0),
            tax_amount=item_data['tax_amount'],
            discount_amount=item_data.get('discount_amount', 0),
            total_amount=item_data['total_amount']
        )
        db.session.add(item)
    
    # Commit transaction
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Bill created successfully',
        'bill_id': bill.id,
        'bill_number': bill.bill_number
    }), 201

@bill_bp.route('/<int:bill_id>/payment', methods=['POST'])
def record_payment(bill_id):
    """
    Record a payment for a bill.
    
    Request body:
    {
        "payment_method": "cash",
        "amount": 100.00,
        "payment_date": "2025-06-03T12:00:00",
        "transaction_reference": "Optional reference",
        "notes": "Optional notes",
        "updated_by": 123  // User or merchant ID
    }
    """
    data = request.json
    
    # Validate required fields
    required_fields = ['payment_method', 'amount']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'success': False,
                'message': f'Missing required field: {field}'
            }), 400
    
    # Get bill
    bill = Bill.query.get(bill_id)
    
    if not bill:
        return jsonify({
            'success': False,
            'message': f'Bill with ID {bill_id} not found'
        }), 404
    
    # Create payment
    payment = Payment(
        bill_id=bill_id,
        payment_method=data['payment_method'],
        amount=data['amount'],
        payment_date=datetime.fromisoformat(data['payment_date']) if 'payment_date' in data else datetime.utcnow(),
        transaction_reference=data.get('transaction_reference'),
        status='completed',
        notes=data.get('notes'),
        updated_by=data.get('updated_by')
    )
    
    db.session.add(payment)
    
    # Update bill status
    payments = Payment.query.filter_by(bill_id=bill_id).all()
    total_paid = sum(p.amount for p in payments) + payment.amount
    
    if total_paid >= bill.total_amount:
        bill.status = 'paid'
    elif total_paid > 0:
        bill.status = 'partially_paid'
    
    bill.updated_at = datetime.utcnow()
    
    # Commit transaction
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Payment recorded successfully',
        'payment_id': payment.id,
        'bill_status': bill.status
    }), 201

@bill_bp.route('/view/<token>', methods=['GET'])
def view_bill_by_token(token):
    """
    View a bill using a temporary token.
    This route is accessed via the temporary link in SMS.
    """
    from src.models.sms_service import SMSService
    
    # Validate token
    result = SMSService.validate_temporary_link(token)
    
    if not result['valid']:
        # If token is invalid, redirect to appropriate page
        return render_template('expired_link.html', reason=result['reason'])
    
    # Get bill
    bill_id = result['bill_id']
    bill = Bill.query.get(bill_id)
    
    if not bill:
        return render_template('error.html', message='Bill not found')
    
    # Get merchant and store
    merchant = Merchant.query.get(bill.merchant_id)
    store = StoreLocation.query.get(bill.store_id) if bill.store_id else None
    
    # Get bill items
    items = BillItem.query.filter_by(bill_id=bill_id).all()
    
    # Get payments
    payments = Payment.query.filter_by(bill_id=bill_id).all()
    total_paid = sum(payment.amount for payment in payments)
    remaining_amount = bill.total_amount - total_paid
    
    # Render bill view template
    return render_template(
        'bill_view.html',
        bill=bill,
        merchant=merchant,
        store=store,
        items=items,
        payments=payments,
        total_paid=total_paid,
        remaining_amount=remaining_amount,
        is_fully_paid=remaining_amount <= 0
    )
