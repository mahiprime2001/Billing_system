# User and Merchant Flows

## Merchant Flows

### 1. Merchant Registration and Onboarding
```
+-------------------+     +-------------------+     +-------------------+
| Create Account    |---->| Complete Profile  |---->| Add Store Details |
| - Email           |     | - Business Name   |     | - Store Location  |
| - Password        |     | - Contact Info    |     | - GST Number      |
| - 2FA Setup       |     | - Business Type   |     | - Store Hours     |
+-------------------+     +-------------------+     +-------------------+
                                                             |
                                                             v
+-------------------+     +-------------------+     +-------------------+
| Start Using       |<----| Set Up Inventory  |<----| Verify Account    |
| Dashboard         |     | - Add Products    |     | - Submit Documents|
|                   |     | - Set Prices      |     | - Admin Approval  |
+-------------------+     +-------------------+     +-------------------+
```

### 2. Bill Creation and Management
```
+-------------------+     +-------------------+     +-------------------+
| Select Customer   |---->| Add Items to Bill |---->| Add Payment Info  |
| - Existing        |     | - From Inventory  |     | - Payment Method  |
| - New Customer    |     | - Custom Items    |     | - Split Payment   |
+-------------------+     +-------------------+     +-------------------+
                                                             |
                                                             v
+-------------------+     +-------------------+     +-------------------+
| View Bill History |<----| Send Bill to User |<----| Finalize Bill     |
| - Status Tracking |     | - SMS Notification|     | - Add Taxes       |
| - Payment Status  |     | - Email Option    |     | - Apply Discounts |
+-------------------+     +-------------------+     +-------------------+
```

### 3. Inventory Management
```
+-------------------+     +-------------------+     +-------------------+
| Add New Products  |---->| Update Inventory  |---->| Set Availability  |
| - Product Details |     | - Stock Levels    |     | - In Stock        |
| - Categories      |     | - Price Changes   |     | - Out of Stock    |
+-------------------+     +-------------------+     +-------------------+
                                                             |
                                                             v
+-------------------+     +-------------------+
| View Inventory    |<----| Generate Reports  |
| - Filter Options  |     | - Stock Levels    |
| - Search          |     | - Popular Items   |
+-------------------+     +-------------------+
```

### 4. Customer Management
```
+-------------------+     +-------------------+     +-------------------+
| Add New Customer  |---->| View Customer List|---->| Customer Details  |
| - Contact Info    |     | - Search          |     | - Purchase History|
| - Address         |     | - Filter          |     | - Payment History |
+-------------------+     +-------------------+     +-------------------+
                                                             |
                                                             v
+-------------------+     +-------------------+
| Send Notifications|<----| Manage Reminders  |
| - Promotions      |     | - Due Bills       |
| - Updates         |     | - Custom Messages |
+-------------------+     +-------------------+
```

### 5. Reporting and Analytics
```
+-------------------+     +-------------------+     +-------------------+
| View Dashboard    |---->| Generate Reports  |---->| Export Data       |
| - Key Metrics     |     | - Sales           |     | - CSV             |
| - Recent Activity |     | - Payments        |     | - PDF             |
+-------------------+     +-------------------+     +-------------------+
                                                             |
                                                             v
+-------------------+
| Analyze Trends    |
| - Sales Patterns  |
| - Customer Behavior|
+-------------------+
```

### 6. Pickup Request Management
```
+-------------------+     +-------------------+     +-------------------+
| Receive Pickup    |---->| Review Request    |---->| Confirm/Reject    |
| Request           |     | - Items           |     | Request           |
| - Notification    |     | - Availability    |     | - With Reason     |
+-------------------+     +-------------------+     +-------------------+
                                                             |
                                                             v
+-------------------+     +-------------------+     +-------------------+
| Prepare Items     |---->| Notify User       |---->| Complete Pickup   |
| - Pack            |     | - Ready Status    |     | - Mark Completed  |
| - Hold            |     | - Pickup Time     |     | - Payment Status  |
+-------------------+     +-------------------+     +-------------------+
```

## User Flows

### 1. User Registration and Onboarding
```
+-------------------+     +-------------------+     +-------------------+
| Create Account    |---->| Complete Profile  |---->| Set Preferences   |
| - Email/Phone     |     | - Personal Info   |     | - Notifications   |
| - Password        |     | - Address         |     | - Privacy Settings|
| - 2FA Setup       |     | - Contact Info    |     |                   |
+-------------------+     +-------------------+     +-------------------+
                                                             |
                                                             v
+-------------------+
| Start Using App   |
| - Tutorial        |
| - Quick Start     |
+-------------------+
```

### 2. Bill Viewing and Management
```
+-------------------+     +-------------------+     +-------------------+
| Receive Bill      |---->| View Bill Details |---->| Record Payment    |
| - SMS Notification|     | - Items           |     | - Payment Method  |
| - App Notification|     | - Taxes           |     | - Split Payment   |
+-------------------+     +-------------------+     +-------------------+
                                                             |
                                                             v
+-------------------+     +-------------------+
| View Bill History |<----| Download/Share    |
| - Status Tracking |     | - PDF             |
| - Payment Status  |     | - Share Options   |
+-------------------+     +-------------------+
```

### 3. Shopping List Management
```
+-------------------+     +-------------------+     +-------------------+
| Create Shopping   |---->| Add Items to List |---->| Save/Edit List    |
| List              |     | - Search Products |     | - Name List       |
| - New List        |     | - Add Custom Items|     | - Set Priority    |
+-------------------+     +-------------------+     +-------------------+
                                                             |
                                                             v
+-------------------+     +-------------------+     +-------------------+
| View Saved Lists  |<----| Share List        |<----| Find Merchants    |
| - Multiple Lists  |     | - With Other Users|     | - Within 10km     |
| - Edit/Delete     |     | - Export          |     | - Route Map       |
+-------------------+     +-------------------+     +-------------------+
```

### 4. List Sharing
```
+-------------------+     +-------------------+     +-------------------+
| Select List       |---->| Choose Sharing    |---->| Select Recipients |
| to Share          |     | Method            |     | - From Contacts   |
| - From Saved Lists|     | - In-App          |     | - By Phone/Email  |
+-------------------+     | - Link            |     +-------------------+
                          +-------------------+              |
                                                             v
+-------------------+     +-------------------+
| Recipient         |<----| Track Sharing     |
| Receives List     |     | Status            |
| - Notification    |     | - Viewed          |
| - Accept/Decline  |     | - Accepted        |
+-------------------+     +-------------------+
```

### 5. Merchant Discovery
```
+-------------------+     +-------------------+     +-------------------+
| Search Merchants  |---->| View Merchant     |---->| Check Inventory   |
| - By Location     |     | Details           |     | - Available Items |
| - By Category     |     | - Store Info      |     | - Prices          |
+-------------------+     +-------------------+     +-------------------+
                                                             |
                                                             v
+-------------------+     +-------------------+
| Get Directions    |<----| Save Favorite     |
| - Route Map       |     | Merchants         |
| - Navigation      |     | - Quick Access    |
+-------------------+     +-------------------+
```

### 6. Route Planning
```
+-------------------+     +-------------------+     +-------------------+
| Select Shopping   |---->| View Suggested    |---->| Customize Route   |
| List              |     | Merchants         |     | - Add/Remove Stops|
| - From Saved Lists|     | - Full Match      |     | - Change Order    |
+-------------------+     | - Partial Matches |     +-------------------+
                          +-------------------+              |
                                                             v
+-------------------+     +-------------------+
| Save Route        |<----| Start Navigation  |
| - For Future Use  |     | - Turn-by-Turn    |
| - Share           |     | - ETA             |
+-------------------+     +-------------------+
```

### 7. Pickup Request
```
+-------------------+     +-------------------+     +-------------------+
| Select Merchant   |---->| Create Pickup     |---->| Specify Details   |
| - From Map        |     | Request           |     | - Pickup Time     |
| - From Favorites  |     | - Select Items    |     | - Special Notes   |
+-------------------+     | - From List/Cart  |     +-------------------+
                          +-------------------+              |
                                                             v
+-------------------+     +-------------------+     +-------------------+
| Track Request     |<----| Receive           |<----| Submit Request    |
| Status            |     | Confirmation      |     | - Review          |
| - Pending/Accepted|     | - Notification    |     | - Confirm         |
| - Ready for Pickup|     | - In-App Update   |     +-------------------+
+-------------------+     +-------------------+
```

## Authentication Flows

### 1. Two-Factor Authentication
```
+-------------------+     +-------------------+     +-------------------+
| Enter Email/Phone |---->| Enter Password    |---->| Enter Auth Code   |
| and Username      |     | (First Factor)    |     | (Second Factor)   |
+-------------------+     +-------------------+     +-------------------+
                                                             |
                                                             v
+-------------------+     +-------------------+
| Session Created   |<----| Remember Device   |
| - JWT Token       |     | - Optional        |
| - Refresh Token   |     | - Device Tracking |
+-------------------+     +-------------------+
```

### 2. Password Reset
```
+-------------------+     +-------------------+     +-------------------+
| Request Password  |---->| Verify Identity   |---->| Create New        |
| Reset             |     | - Email Code      |     | Password          |
| - Email/Phone     |     | - SMS Code        |     | - Password Rules  |
+-------------------+     +-------------------+     +-------------------+
                                                             |
                                                             v
+-------------------+
| Reset Complete    |
| - Confirmation    |
| - Login Prompt    |
+-------------------+
```

## Notification Flows

### 1. SMS Notification
```
+-------------------+     +-------------------+     +-------------------+
| Trigger Event     |---->| Generate Message  |---->| Send SMS          |
| - New Bill        |     | - Template        |     | - Via SMS Gateway |
| - Payment Due     |     | - Personalization |     | - Delivery Status |
+-------------------+     +-------------------+     +-------------------+
                                                             |
                                                             v
+-------------------+     +-------------------+
| Track Delivery    |<----| User Interaction  |
| - Sent Status     |     | - View Bill       |
| - Delivery Status |     | - Make Payment    |
+-------------------+     +-------------------+
```

### 2. In-App Notification
```
+-------------------+     +-------------------+     +-------------------+
| Trigger Event     |---->| Create            |---->| Deliver to User   |
| - New Bill        |     | Notification      |     | - Push Notification|
| - Merchant Update |     | - Content         |     | - In-App Alert    |
+-------------------+     +-------------------+     +-------------------+
                                                             |
                                                             v
+-------------------+     +-------------------+
| Track Status      |<----| User Action       |
| - Delivered       |     | - Open            |
| - Read            |     | - Dismiss         |
+-------------------+     +-------------------+
```

## Payment Recording Flows

### 1. Merchant Records Payment
```
+-------------------+     +-------------------+     +-------------------+
| Select Bill       |---->| Enter Payment     |---->| Record Payment    |
| - From List       |     | Details           |     | Method            |
| - Search          |     | - Amount          |     | - UPI/Card/Cash   |
+-------------------+     | - Date            |     | - Split Payment   |
                          +-------------------+     +-------------------+
                                                             |
                                                             v
+-------------------+     +-------------------+
| Update Bill Status|<----| Send Confirmation |
| - Paid/Partial    |     | - To User         |
| - Outstanding     |     | - Receipt         |
+-------------------+     +-------------------+
```

### 2. User Records Payment
```
+-------------------+     +-------------------+     +-------------------+
| View Bill         |---->| Record Payment    |---->| Confirm Payment   |
| - From List       |     | - Payment Method  |     | Details           |
| - From Notification|    | - Amount          |     | - Review          |
+-------------------+     | - Date            |     | - Submit          |
                          +-------------------+     +-------------------+
                                                             |
                                                             v
+-------------------+     +-------------------+
| Payment Recorded  |<----| Merchant Notified |
| - Status Updated  |     | - For Verification|
| - Receipt         |     | - Approval        |
+-------------------+     +-------------------+
```

These flow diagrams outline the key user journeys and system processes for both merchants and users in the billing system. They cover the core functionality as well as the additional features like shopping list management, merchant discovery, route planning, list sharing between users, and item pickup requests.
