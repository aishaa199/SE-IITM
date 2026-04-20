# Glow Suite — Salon Management System

A full-stack salon management platform with role-based dashboards for Owners, Managers, Staff, and Customers. Handles appointment scheduling, inventory management, staff attendance, automated invoicing, analytics, and customer rewards.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Environment Variables](#environment-variables)
- [Default Credentials](#default-credentials)
- [API Overview](#api-overview)
- [Testing](#testing)
- [License](#license)

---

## Features

- **Role-based access** — Owner, Manager, Staff, and Customer portals
- **Appointment management** — booking, rescheduling, cancellation, and status tracking
- **Invoicing** — PDF invoice generation and email delivery to customers
- **Inventory & procurement** — stock tracking, low-stock alerts, wholesaler order PDFs
- **Staff attendance** — automated threshold-based absence marking via scheduler
- **Customer rewards** — points accrual, redemption, and VIP tier tracking
- **Analytics & reports** — sales, staff performance, and appointment CSV exports
- **Notifications** — in-app notifications for managers, staff, and customers
- **Forgot password** — email-based password reset for all roles
- **AI assistant** — Claude-powered insights on the manager dashboard

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Vue 3, Vite, Pinia, Vue Router |
| Backend | Flask, Flask-RESTful, Flask-Security-Too |
| Database | SQLite (via Flask-SQLAlchemy) |
| Auth | Flask-Security token-based auth (bcrypt) |
| Email | Flask-Mail (Gmail SMTP) |
| Scheduling | Flask-APScheduler |
| AI | Anthropic Claude API |
| Testing | Pytest |

---

## Project Structure

```
SE-IITM/
├── backend/
│   ├── application/
│   │   ├── __init__.py
│   │   ├── models.py            # SQLAlchemy ORM models
│   │   ├── views.py             # Auth & password reset routes
│   │   ├── resources.py         # Flask-RESTful API resources
│   │   ├── tasks.py             # Scheduled background jobs
│   │   ├── report_generators.py # CSV report generation
│   │   └── sec.py               # Flask-Security datastore setup
│   ├── instance/                # SQLite database (auto-created)
│   ├── tests/                   # Pytest test suite
│   ├── customer_invoices/       # Generated invoice PDFs
│   ├── wholesaler_orders/       # Generated order PDFs
│   ├── config.py                # App configuration
│   ├── main.py                  # Application entry point
│   ├── upload_initial_data.py   # Seed data loader
│   ├── upload_salon_config.py   # Salon config seeder
│   ├── seed_dummy_data.py       # Dummy data for development
│   ├── openapi.yaml             # OpenAPI specification
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── views/
│   │   │   ├── HomePage.vue
│   │   │   ├── LoginView.vue
│   │   │   ├── ResetPasswordView.vue
│   │   │   ├── DashboardView.vue    # Manager dashboard
│   │   │   ├── StaffDashboard.vue
│   │   │   ├── CustomerDashboard.vue
│   │   │   └── OwnerDashboard.vue
│   │   ├── stores/
│   │   │   └── appStore.js          # Pinia auth store
│   │   ├── router/
│   │   │   └── index.js             # Vue Router routes & guards
│   │   ├── api/
│   │   │   └── apiClient.js         # Axios/fetch wrapper
│   │   ├── styles/
│   │   │   └── global.css
│   │   ├── App.vue
│   │   └── main.js
│   ├── public/
│   ├── index.html
│   └── vite.config.js
├── reports/                         # Generated CSV reports
��── Testing_guide.md
├── LICENSE
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 18+ and npm

### Backend Setup

```bash
cd backend

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment variables
cp .env.example .env             # then edit .env with your values

# Start the server
python main.py
```

The backend will be available at `http://127.0.0.1:5000`.

> The database is created automatically on first run. Default salon configuration and seed data are loaded if the database does not exist.

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:5173`.

---

## Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# AI
ANTHROPIC_API_KEY=your_anthropic_api_key

# Email (Gmail SMTP — use an App Password if 2-Step Verification is enabled)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_DEFAULT_SENDER=your_email@gmail.com

# Frontend base URL (used in password reset emails)
FRONTEND_URL=http://localhost:5173
```

> **Gmail App Password**: If your Google account has 2-Step Verification enabled, generate an App Password at *Google Account → Security → 2-Step Verification → App passwords* and use it as `MAIL_PASSWORD`.

---

## Default Credentials

| Role | Username | Password |
|---|---|---|
| Owner | `owner` | `owner` |
| Manager | `manager` | `manager` |
| Staff | *(set by manager)* | *(set on creation)* |
| Customer | *(email address)* | *(set on registration)* |

> Change default credentials after first login in a production environment.

---

## API Overview

All REST endpoints are prefixed with `/api/`. Auth endpoints are at the root.

| Method | Endpoint | Description |
|---|---|---|
| POST | `/owner-login` | Owner authentication |
| POST | `/manager-login` | Manager authentication |
| POST | `/staff-login` | Staff authentication |
| POST | `/customer-login` | Customer authentication |
| POST | `/register-customer` | Customer self-registration |
| POST | `/forgot-password` | Request password reset email |
| POST | `/reset-password` | Reset password with token |
| POST | `/logout` | Invalidate auth token |
| GET | `/api/get-all-invoices` | Fetch all invoices |
| GET | `/api/generate-invoice-pdf/<id>` | Generate and email invoice PDF |
| GET | `/api/appointments` | List appointments |
| GET | `/api/staff` | List staff members |
| GET | `/api/customers` | List customers |

---

## Testing

```bash
cd backend
source .venv/bin/activate
pytest
```

Test files are in `backend/tests/`. See [Testing_guide.md](Testing_guide.md) for a detailed guide.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
