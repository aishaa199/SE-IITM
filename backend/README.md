# Backend Documentation - Salon Management System

This repository contains the backend for the Salon Management System, built with **Flask**, **Flask-RESTful**, and **Flask-Security-Too**.

## 🛠 Tech Stack
- **Framework**: Flask / Flask-RESTful
- **Authentication**: Flask-Security-Too (Token-based)
- **Database**: SQLite (via Flask-SQLAlchemy)
- **Environment**: Python 3.x
- **Cross-Origin Resource Sharing (CORS)**: Enabled via `flask-cors`

## 📂 Project Structure
```text
backend/
├── application/
│   ├── models.py      # SQLAlchemy DB models (User, Staff, Customer, etc.)
│   ├── resources.py    # Flask-RESTful resources and common routes
│   ├── sec.py         # Flask-Security setup (UserDatastore)
│   └── views.py       # Standard Flask routes and blueprints
├── config.py          # Configuration settings (Dev/Prod)
├── main.py            # Application entry point and app factory
├── requirements.txt    # Python dependencies
└── upload_initial_data.py # Script to seed the database
```

## 🚀 Getting Started

### 1. Set Up Environment
It is recommended to use a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
The application runs on `http://localhost:5000` by default.
```bash
python main.py
```
If you are running this application for the first time, please run the one time data  setup script.
```bash
python upload_initial_data.py
```

## 🔐 API Reference

### User Authentication
All secured routes require an `Authentication-Token` header.

### Common Routes
- `PUT /api/change-password`: A unified route for all users (Owners, Managers, Staff, Customers) to update their passwords.
    - **Header**: `Authentication-Token: <token>`
    - **Body**:
      ```json
      {
        "current_password": "oldpassword",
        "new_password": "newpassword123",
        "confirm_password": "newpassword123"
      }
      ```

### Owner Routes
- `POST /api/create-manager`: Allows owners to register new managers.


## 📝 Configuration
- **Database**: The database file is located in the `instance/` folder.
- **Port**: Configured in `main.py` (Default: 5000).
- **Debug Mode**: Enabled by default in the `DevelopmentConfig`.
