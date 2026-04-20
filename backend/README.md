# Glow Suite Backend

The backend of Glow Suite is a Flask-based RESTful API designed to manage luxury beauty salon operations, including staff scheduling, inventory, appointment booking, and reporting.

## Project Structure

```text
backend/
├── application/             # Core application logic
│   ├── models.py            # SQLAlchemy database models
│   ├── resources.py         # Flask-RESTful API resources (endpoints)
│   ├── routes.py            # Standard Flask views and routes
│   ├── tasks.py             # Periodic and background tasks (APScheduler)
│   ├── sec.py               # Flask-Security setup (authentication/authorization)
│   └── report_generators.py # Logic for generating PDF and CSV reports
├── tests/                   # Pytest-based test suite
│   ├── conftest.py          # Test configuration and fixtures
│   └── test_*.py            # Comprehensive unit and integration tests
├── instance/                # Local database and instance-specific files
├── reports/                 # Generated business reports (CSV/PDF)
├── customer_invoices/       # Generated PDF invoices for customers
├── wholesaler_orders/       # Generated PDF replenishment orders for suppliers
├── config.py                # Environment-specific configuration
├── main.py                  # Application entry point and factory
├── requirements.txt         # Project dependencies
└── seed_dummy_data.py       # Script to populate the database with initial data
```

## Technologies Used

- **Flask**: Main web framework.
- **Flask-RESTful**: Extension for building REST APIs.
- **SQLAlchemy**: ORM for database management.
- **Flask-Security-Too**: Comprehensive security for authentication and role-based access control.
- **APScheduler**: For managing recurring tasks like cleaning up history and sending reminders.
- **FPDF2**: For generating PDF invoices and reports.
- **Pytest**: For robust automated testing.

## Getting Started

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)

### Installation

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run initial configuration and data upload scripts:
   ```bash
   python upload_salon_config.py
   python upload_initial_data.py
   ```

4. Initialize the database and seed data:
   The application will automatically create the database and seed initial data on its first run via the `create_app` factory in `main.py`.

### Running the Application

To start the development server:
```bash
python main.py
```
The API will be available at `http://localhost:5000/api`.

## Testing

Run the full test suite using `pytest`:
```bash
pytest
```

## Key API Features

- **RBAC**: Role-based access control (Owner, Manager, Staff, Customer).
- **Inventory Management**: Track product stock levels and automate replenishment orders.
- **Appointment System**: Manage services, schedules, and customer history.
- **Invoicing**: Generate PDF invoices for completed appointments.
- **Reporting**: Automated generation of monthly/weekly sales and staff performance reports.
