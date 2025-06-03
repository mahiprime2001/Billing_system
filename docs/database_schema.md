# Database Schema for Billing System

## Overview

This document outlines the database schema for the billing system, designed to support all the required features including bill management, user and merchant accounts, inventory tracking, shopping lists, and geolocation services.

## Database Technology

PostgreSQL with PostGIS extension for geospatial capabilities.

## Schema Design

### Users Table

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(15) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    profile_image_url VARCHAR(255),
    preferred_payment_method VARCHAR(50),
    default_address_id INTEGER
);
```

### User Authentication Table

```sql
CREATE TABLE user_authentication (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    auth_type VARCHAR(20) NOT NULL, -- 'password', 'google_auth', 'microsoft_auth', etc.
    auth_key VARCHAR(255), -- For storing authenticator app keys
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_used TIMESTAMP
);
```

### User Addresses Table

```sql
CREATE TABLE user_addresses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    address_line1 VARCHAR(100) NOT NULL,
    address_line2 VARCHAR(100),
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    country VARCHAR(50) NOT NULL DEFAULT 'India',
    is_default BOOLEAN DEFAULT FALSE,
    label VARCHAR(50), -- 'home', 'work', etc.
    location GEOGRAPHY(POINT), -- PostGIS point for geolocation
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Merchants Table

```sql
CREATE TABLE merchants (
    id SERIAL PRIMARY KEY,
    business_name VARCHAR(100) NOT NULL,
    gst_number VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(15) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    contact_person VARCHAR(100),
    business_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    logo_url VARCHAR(255),
    website_url VARCHAR(255)
);
```

### Merchant Authentication Table

```sql
CREATE TABLE merchant_authentication (
    id SERIAL PRIMARY KEY,
    merchant_id INTEGER REFERENCES merchants(id) ON DELETE CASCADE,
    auth_type VARCHAR(20) NOT NULL, -- 'password', 'google_auth', 'microsoft_auth', etc.
    auth_key VARCHAR(255), -- For storing authenticator app keys
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_used TIMESTAMP
);
```

### Store Locations Table

```sql
CREATE TABLE store_locations (
    id SERIAL PRIMARY KEY,
    merchant_id INTEGER REFERENCES merchants(id) ON DELETE CASCADE,
    store_name VARCHAR(100) NOT NULL,
    address_line1 VARCHAR(100) NOT NULL,
    address_line2 VARCHAR(100),
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    country VARCHAR(50) NOT NULL DEFAULT 'India',
    location GEOGRAPHY(POINT) NOT NULL, -- PostGIS point for geolocation
    contact_number VARCHAR(15),
    opening_time TIME,
    closing_time TIME,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Store Operating Hours Table

```sql
CREATE TABLE store_operating_hours (
    id SERIAL PRIMARY KEY,
    store_id INTEGER REFERENCES store_locations(id) ON DELETE CASCADE,
    day_of_week INTEGER NOT NULL, -- 0 = Sunday, 1 = Monday, etc.
    opening_time TIME NOT NULL,
    closing_time TIME NOT NULL,
    is_closed BOOLEAN DEFAULT FALSE
);
```

### Product Categories Table

```sql
CREATE TABLE product_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    parent_category_id INTEGER REFERENCES product_categories(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Products Table

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    category_id INTEGER REFERENCES product_categories(id),
    base_price DECIMAL(10, 2) NOT NULL,
    tax_rate DECIMAL(5, 2) DEFAULT 0,
    sku VARCHAR(50),
    barcode VARCHAR(50),
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Merchant Inventory Table

```sql
CREATE TABLE merchant_inventory (
    id SERIAL PRIMARY KEY,
    merchant_id INTEGER REFERENCES merchants(id) ON DELETE CASCADE,
    store_id INTEGER REFERENCES store_locations(id),
    product_id INTEGER REFERENCES products(id),
    stock_quantity INTEGER NOT NULL DEFAULT 0,
    price DECIMAL(10, 2) NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    last_restocked TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(merchant_id, store_id, product_id)
);
```

### Bills Table

```sql
CREATE TABLE bills (
    id SERIAL PRIMARY KEY,
    bill_number VARCHAR(20) UNIQUE NOT NULL,
    merchant_id INTEGER REFERENCES merchants(id) ON DELETE CASCADE,
    store_id INTEGER REFERENCES store_locations(id),
    user_id INTEGER REFERENCES users(id),
    bill_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    due_date TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL,
    tax_amount DECIMAL(10, 2) NOT NULL DEFAULT 0,
    discount_amount DECIMAL(10, 2) NOT NULL DEFAULT 0,
    status VARCHAR(20) NOT NULL DEFAULT 'pending', -- 'pending', 'paid', 'partially_paid', 'overdue', 'cancelled'
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Bill Items Table

```sql
CREATE TABLE bill_items (
    id SERIAL PRIMARY KEY,
    bill_id INTEGER REFERENCES bills(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id),
    product_name VARCHAR(100) NOT NULL, -- Stored separately in case product details change
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    tax_rate DECIMAL(5, 2) NOT NULL DEFAULT 0,
    tax_amount DECIMAL(10, 2) NOT NULL DEFAULT 0,
    discount_amount DECIMAL(10, 2) NOT NULL DEFAULT 0,
    total_amount DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Payments Table

```sql
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    bill_id INTEGER REFERENCES bills(id) ON DELETE CASCADE,
    payment_method VARCHAR(50) NOT NULL, -- 'cash', 'upi', 'card', etc.
    amount DECIMAL(10, 2) NOT NULL,
    payment_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    transaction_reference VARCHAR(100),
    status VARCHAR(20) NOT NULL DEFAULT 'completed', -- 'completed', 'pending', 'failed', 'refunded'
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by INTEGER -- User or merchant who recorded the payment
);
```

### Shopping Lists Table

```sql
CREATE TABLE shopping_lists (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Shopping List Items Table

```sql
CREATE TABLE shopping_list_items (
    id SERIAL PRIMARY KEY,
    list_id INTEGER REFERENCES shopping_lists(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id),
    custom_item_name VARCHAR(100), -- For items not in the product database
    quantity INTEGER NOT NULL DEFAULT 1,
    is_purchased BOOLEAN DEFAULT FALSE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### List Sharing Table

```sql
CREATE TABLE list_sharing (
    id SERIAL PRIMARY KEY,
    list_id INTEGER REFERENCES shopping_lists(id) ON DELETE CASCADE,
    shared_by INTEGER REFERENCES users(id) ON DELETE CASCADE,
    shared_with INTEGER REFERENCES users(id) ON DELETE CASCADE,
    shared_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    access_level VARCHAR(20) DEFAULT 'view', -- 'view', 'edit'
    status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'accepted', 'declined'
    last_accessed TIMESTAMP,
    UNIQUE(list_id, shared_with)
);
```

### Pickup Requests Table

```sql
CREATE TABLE pickup_requests (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    merchant_id INTEGER REFERENCES merchants(id) ON DELETE CASCADE,
    store_id INTEGER REFERENCES store_locations(id),
    status VARCHAR(20) NOT NULL DEFAULT 'pending', -- 'pending', 'accepted', 'ready', 'completed', 'cancelled'
    requested_pickup_time TIMESTAMP,
    actual_pickup_time TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Pickup Request Items Table

```sql
CREATE TABLE pickup_request_items (
    id SERIAL PRIMARY KEY,
    pickup_request_id INTEGER REFERENCES pickup_requests(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id),
    custom_item_name VARCHAR(100), -- For items not in the product database
    quantity INTEGER NOT NULL DEFAULT 1,
    status VARCHAR(20) NOT NULL DEFAULT 'pending', -- 'pending', 'available', 'unavailable', 'substituted'
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Notifications Table

```sql
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    merchant_id INTEGER REFERENCES merchants(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL, -- 'bill', 'payment', 'pickup', etc.
    title VARCHAR(100) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    related_entity_type VARCHAR(50), -- 'bill', 'payment', 'pickup', etc.
    related_entity_id INTEGER, -- ID of the related entity
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### SMS Notifications Table

```sql
CREATE TABLE sms_notifications (
    id SERIAL PRIMARY KEY,
    phone_number VARCHAR(15) NOT NULL,
    message TEXT NOT NULL,
    temporary_link VARCHAR(255),
    link_expiry TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'sent', 'delivered', 'failed'
    related_entity_type VARCHAR(50), -- 'bill', 'payment', 'pickup', etc.
    related_entity_id INTEGER, -- ID of the related entity
    sent_at TIMESTAMP,
    delivery_status_updated_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Temporary Links Table

```sql
CREATE TABLE temporary_links (
    id SERIAL PRIMARY KEY,
    token VARCHAR(255) UNIQUE NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    related_entity_type VARCHAR(50) NOT NULL, -- 'bill', 'payment', etc.
    related_entity_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL, -- 48 hours after creation
    is_accessed BOOLEAN DEFAULT FALSE,
    first_accessed_at TIMESTAMP,
    access_count INTEGER DEFAULT 0,
    last_accessed_at TIMESTAMP,
    is_revoked BOOLEAN DEFAULT FALSE,
    revoked_at TIMESTAMP
);
```

### Routes Table

```sql
CREATE TABLE routes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100),
    start_location GEOGRAPHY(POINT),
    end_location GEOGRAPHY(POINT),
    total_distance DECIMAL(10, 2), -- in kilometers
    estimated_time INTEGER, -- in minutes
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Route Stops Table

```sql
CREATE TABLE route_stops (
    id SERIAL PRIMARY KEY,
    route_id INTEGER REFERENCES routes(id) ON DELETE CASCADE,
    store_id INTEGER REFERENCES store_locations(id),
    stop_order INTEGER NOT NULL,
    location GEOGRAPHY(POINT) NOT NULL,
    estimated_arrival_time TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Sessions Table

```sql
CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    merchant_id INTEGER REFERENCES merchants(id) ON DELETE CASCADE,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    refresh_token VARCHAR(255) UNIQUE,
    ip_address VARCHAR(45),
    user_agent TEXT,
    device_info TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    last_activity TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);
```

## Indexes

```sql
-- Users indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_phone_number ON users(phone_number);

-- Merchants indexes
CREATE INDEX idx_merchants_business_name ON merchants(business_name);
CREATE INDEX idx_merchants_gst_number ON merchants(gst_number);

-- Store locations indexes
CREATE INDEX idx_store_locations_merchant_id ON store_locations(merchant_id);
CREATE INDEX idx_store_locations_location ON store_locations USING GIST(location);

-- Products indexes
CREATE INDEX idx_products_name ON products(name);
CREATE INDEX idx_products_category_id ON products(category_id);

-- Inventory indexes
CREATE INDEX idx_merchant_inventory_merchant_id ON merchant_inventory(merchant_id);
CREATE INDEX idx_merchant_inventory_product_id ON merchant_inventory(product_id);
CREATE INDEX idx_merchant_inventory_store_id ON merchant_inventory(store_id);

-- Bills indexes
CREATE INDEX idx_bills_merchant_id ON bills(merchant_id);
CREATE INDEX idx_bills_user_id ON bills(user_id);
CREATE INDEX idx_bills_bill_date ON bills(bill_date);
CREATE INDEX idx_bills_status ON bills(status);

-- Payments indexes
CREATE INDEX idx_payments_bill_id ON payments(bill_id);
CREATE INDEX idx_payments_payment_date ON payments(payment_date);

-- Shopping lists indexes
CREATE INDEX idx_shopping_lists_user_id ON shopping_lists(user_id);

-- Pickup requests indexes
CREATE INDEX idx_pickup_requests_user_id ON pickup_requests(user_id);
CREATE INDEX idx_pickup_requests_merchant_id ON pickup_requests(merchant_id);
CREATE INDEX idx_pickup_requests_status ON pickup_requests(status);

-- Notifications indexes
CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_merchant_id ON notifications(merchant_id);
CREATE INDEX idx_notifications_created_at ON notifications(created_at);

-- Temporary links indexes
CREATE INDEX idx_temporary_links_token ON temporary_links(token);
CREATE INDEX idx_temporary_links_expires_at ON temporary_links(expires_at);
```

## Relationships Diagram

```
Users 1──┐
         │
         ├──n User_Authentication
         │
         ├──n User_Addresses
         │
         ├──n Shopping_Lists ───┐
         │                      │
         │                      ├──n Shopping_List_Items
         │                      │
         │                      └──n List_Sharing
         │
         ├──n Bills ───┐
         │             │
         │             ├──n Bill_Items
         │             │
         │             └──n Payments
         │
         ├──n Pickup_Requests ───n Pickup_Request_Items
         │
         ├──n Notifications
         │
         ├──n SMS_Notifications
         │
         ├──n Temporary_Links
         │
         ├──n Routes ───n Route_Stops
         │
         └──n Sessions

Merchants 1──┐
             │
             ├──n Merchant_Authentication
             │
             ├──n Store_Locations ───n Store_Operating_Hours
             │
             ├──n Merchant_Inventory
             │
             ├──n Bills
             │
             ├──n Pickup_Requests
             │
             ├──n Notifications
             │
             └──n Sessions

Products 1──┐
            │
            ├──n Merchant_Inventory
            │
            ├──n Bill_Items
            │
            ├──n Shopping_List_Items
            │
            └──n Pickup_Request_Items

Product_Categories 1──n Products
```

## Notes on Schema Design

1. **Geospatial Features**:
   - The `location` columns in `user_addresses` and `store_locations` use PostGIS's `GEOGRAPHY(POINT)` type for accurate distance calculations.
   - This enables the 10km radius search functionality for finding merchants.

2. **Authentication**:
   - Separate authentication tables for users and merchants support multiple authentication methods.
   - Two-factor authentication is supported through the `auth_type` and `auth_key` fields.

3. **Temporary Links**:
   - The `temporary_links` table tracks all generated temporary links for SMS notifications.
   - Links expire after 48 hours as specified by the `expires_at` field.
   - Access tracking helps with analytics and security monitoring.

4. **Shopping List Sharing**:
   - The `list_sharing` table enables users to share shopping lists with other users.
   - Different access levels can be granted (view-only or edit).

5. **Pickup Requests**:
   - The `pickup_requests` and `pickup_request_items` tables handle the feature where users can request items for later pickup.
   - Status tracking allows both users and merchants to monitor the request lifecycle.

6. **Payment Tracking**:
   - The `payments` table supports recording multiple payment methods for a single bill.
   - This enables tracking split payments (e.g., part cash, part UPI).

7. **Route Planning**:
   - The `routes` and `route_stops` tables support the feature where users can plan routes to visit multiple merchants.
   - This integrates with the shopping list feature to optimize shopping trips.

This schema design provides a comprehensive foundation for the billing system, supporting all the required features while maintaining data integrity and performance.
