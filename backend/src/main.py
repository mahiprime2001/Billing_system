import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # DON'T CHANGE THIS !!!

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import jwt
from datetime import datetime, timedelta

# Import models
from src.models.user import db as user_db
from src.models.merchant import db as merchant_db
from src.models.product import db as product_db
from src.models.bill import db as bill_db
from src.models.shopping_list import db as shopping_list_db
from src.models.pickup_request import db as pickup_request_db
from src.models.notification import db as notification_db
from src.models.sms_service import db as sms_db

# Import routes
from src.routes.bill import bill_bp
from src.routes.sms import sms_bp

app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///billing_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Register blueprints
app.register_blueprint(bill_bp, url_prefix='/api/bills')
app.register_blueprint(sms_bp, url_prefix='/api/sms')

# Initialize models with the app
with app.app_context():
    user_db.init_app(app)
    merchant_db.init_app(app)
    product_db.init_app(app)
    bill_db.init_app(app)
    shopping_list_db.init_app(app)
    pickup_request_db.init_app(app)
    notification_db.init_app(app)
    sms_db.init_app(app)
    
    # Create all tables
    db.create_all()

@app.route('/')
def index():
    return jsonify({
        'message': 'Welcome to the Billing System API',
        'version': '1.0.0',
        'status': 'running'
    })

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
