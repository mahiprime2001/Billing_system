# Billing System Project

## Overview
The Billing System project is designed to streamline the process of managing bills, merchants, notifications, and user interactions. It consists of a backend and frontend system, along with comprehensive documentation to support development and maintenance.

## Project Structure

### Backend
The backend is implemented in Python and is structured as follows:

- **requirements.txt**: Contains the dependencies required for the backend.
- **instance/**: Configuration and instance-specific files.
- **src/**: Main source code directory.
  - **models/**: Contains Python files for managing entities like bills, merchants, notifications, pickup requests, products, shopping lists, SMS services, and users.
  - **routes/**: Defines API routes for bills, SMS, and user-related operations.
  - **static/**: Contains static files like `index.html`.

### Frontend
The frontend is implemented using modern web technologies and frameworks, including React and Tailwind CSS. It is structured as follows:

- **user-app/**: Main frontend application.
  - **components/**: Contains React components for managing bills, merchants, shopping lists, and UI elements.
  - **hooks/**: Custom React hooks.
  - **lib/**: Utility functions.
  - **public/**: Public assets like `vite.svg`.
  - **src/**: Main source code directory.
    - **App.tsx**: Entry point for the React application.
    - **index.css**: Global styles.
    - **vite-env.d.ts**: TypeScript environment definitions.

### Documentation
The `docs/` folder contains detailed documentation:

- **database_schema.md**: Database design and schema.
- **sms_notification_system.md**: Details about the SMS notification system.
- **system_architecture.md**: Overview of the system architecture.
- **user_merchant_flows.md**: User and merchant interaction flows.
- **validation_report.md**: Validation and testing reports.

## Key Features

### Backend
- **Bill Management**: Create, update, and manage bills.
- **Merchant Integration**: Find and interact with merchants.
- **Notification System**: Send SMS notifications.
- **User Management**: Handle user data and interactions.

### Frontend
- **User-Friendly Interface**: Intuitive UI for managing bills and shopping lists.
- **React Components**: Modular and reusable components.
- **Tailwind CSS**: Modern styling framework.

## Setup Instructions

### Backend
1. Navigate to the `backend/` directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the backend server:
   ```bash
   python src/main.py
   ```

### Frontend
1. Navigate to the `frontend/user-app/` directory.
2. Install dependencies:
   ```bash
   pnpm install
   ```
3. Start the development server:
   ```bash
   pnpm dev
   ```

## Contributing
Contributions are welcome! Please follow the guidelines outlined in the `CONTRIBUTING.md` file (if available).

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact
For any questions or support, please contact the project maintainer.
