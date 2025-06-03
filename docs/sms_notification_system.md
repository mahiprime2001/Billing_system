# SMS Notification System with Temporary Links

## Overview

This document outlines the design for the SMS notification system with temporary links that expire after 48 hours. This feature ensures that users can quickly access their bills via SMS while maintaining security through time-limited access.

## System Components

### 1. SMS Notification Service

- **Purpose**: Generate and send SMS notifications with temporary links
- **Technology**: Integration with SMS gateway APIs (Twilio, etc.)
- **Key Features**:
  - Template-based message generation
  - Personalization with user details
  - Temporary link generation
  - Delivery status tracking

### 2. Temporary Link Generation

- **Purpose**: Create secure, time-limited links to bills
- **Technology**: JWT or similar token-based system
- **Key Features**:
  - Unique link generation per bill
  - Embedded expiration timestamp (48 hours)
  - Encrypted bill identifier
  - Protection against tampering

### 3. Link Validation Service

- **Purpose**: Validate temporary links when accessed
- **Technology**: Server-side validation middleware
- **Key Features**:
  - Token decryption and validation
  - Expiration time checking
  - Redirect to appropriate bill view
  - Graceful handling of expired links

## Workflow

### 1. SMS Notification Flow with Temporary Links

```
+-------------------+     +-------------------+     +-------------------+
| Trigger Event     |---->| Generate Temporary|---->| Create SMS with   |
| - New Bill        |     | Link              |     | Link              |
| - Payment Due     |     | - 48hr Expiry     |     | - Message Template|
+-------------------+     | - Secure Token    |     | - Personalization |
                          +-------------------+     +-------------------+
                                                             |
                                                             v
+-------------------+     +-------------------+     +-------------------+
| Track Link        |<----| Track Delivery    |<----| Send SMS          |
| Usage             |     | - Sent Status     |     | - Via SMS Gateway |
| - Clicks          |     | - Delivery Status |     | - Delivery Status |
| - Expiration      |     +-------------------+     +-------------------+
+-------------------+
```

### 2. Link Access Flow

```
+-------------------+     +-------------------+     +-------------------+
| User Clicks       |---->| Validate Link     |---->| If Valid: Show    |
| Temporary Link    |     | - Decrypt Token   |     | Bill              |
| - From SMS        |     | - Check Expiry    |     | - Bill Details    |
+-------------------+     +-------------------+     | - Payment Options |
                                  |                 +-------------------+
                                  |
                                  v
                          +-------------------+
                          | If Expired:       |
                          | Show Expiry Page  |
                          | - App Download    |
                          | - Login Prompt    |
                          +-------------------+
```

## Technical Implementation

### 1. Temporary Link Generation

```python
def generate_temporary_link(bill_id, user_id):
    # Create payload with bill ID and expiration time (48 hours from now)
    expiration_time = datetime.now() + timedelta(hours=48)
    
    payload = {
        'bill_id': bill_id,
        'user_id': user_id,
        'exp': expiration_time.timestamp()
    }
    
    # Generate JWT token
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    
    # Create link with token
    link = f"{BASE_URL}/bills/view/{token}"
    
    # Store link metadata in database for tracking
    store_link_metadata(bill_id, user_id, token, expiration_time)
    
    return link
```

### 2. Link Validation

```python
def validate_temporary_link(token):
    try:
        # Decode and validate token
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        
        # Check if token has expired
        current_time = datetime.now().timestamp()
        if current_time > payload['exp']:
            return {
                'valid': False,
                'reason': 'expired',
                'redirect_to': '/expired-link'
            }
        
        # Token is valid, return bill information
        bill_id = payload['bill_id']
        user_id = payload['user_id']
        
        # Log access for analytics
        log_link_access(token, bill_id, user_id)
        
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
```

### 3. Expired Link Handling

```python
def handle_expired_link():
    # Generate response for expired link
    response = {
        'message': 'This link has expired. Bills are available for 48 hours via SMS links.',
        'options': [
            {
                'text': 'Download our app',
                'link': APP_DOWNLOAD_LINK
            },
            {
                'text': 'Log in to view all bills',
                'link': LOGIN_PAGE_LINK
            }
        ]
    }
    
    return response
```

## Security Considerations

1. **Token Security**:
   - Use strong encryption for JWT tokens
   - Include minimal necessary information in payload
   - Implement token blacklisting for revocation if needed

2. **Link Protection**:
   - Implement rate limiting to prevent brute force attacks
   - Use HTTPS for all link access
   - Validate user identity when possible

3. **Data Protection**:
   - Ensure sensitive bill information is properly secured
   - Implement proper access controls
   - Log all access attempts for audit purposes

## User Experience

1. **SMS Content**:
   - Clear indication of temporary nature: "View your bill (link valid for 48 hours)"
   - Brief bill summary (merchant, amount)
   - Call to action to download the app for permanent access

2. **Expired Link Page**:
   - Clear explanation of expiration
   - Prominent app download option
   - Login option for web access
   - Contact information for support

## Implementation Considerations

1. **Database Storage**:
   - Track all generated links
   - Record access patterns
   - Enable analytics on link usage

2. **Performance**:
   - Optimize token validation for quick response
   - Cache frequently accessed bills
   - Implement efficient token verification

3. **Monitoring**:
   - Track link generation and usage
   - Monitor expiration patterns
   - Alert on unusual access patterns

This design ensures that users can conveniently access their bills via SMS while maintaining security through time-limited access. The permanent availability of bills in the application provides a reliable alternative for long-term access.
