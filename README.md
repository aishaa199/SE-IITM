
# Frontend Application

A Vue.js 3 frontend application built with Vite for managing manager, customer, staff, and owner dashboards.

## Prerequisites

- **Node.js**: v20.19.0 or v22.12.0+
- **npm**: Included with Node.js

## Installation

### 1. Change Directory

Navigate to the frontend folder:

```sh
cd frontend
```

### 2. Install Dependencies

Install all required npm packages:

```sh
npm install
```

## Running the Application

### Development Server

Start the development server with hot module replacement:

```sh
npm run dev
```

The application will typically run at `http://localhost:5173`


## Viewing Different Dashboards

Once the development server is running, you can access different dashboard views:

- **Manager Dashboard**: `http://localhost:5173/test/manager`
- **Staff Dashboard**: `http://localhost:5173/test/staff`
- **Customer Dashboard**: `http://localhost:5173/test/customer`
- **Owner Dashboard**: `http://localhost:5173/test/owner`

## Project Structure

- `src/` - Source files
  - `components/` - Reusable Vue components
  - `views/` - Page components
  - `router/` - Vue Router configuration
  - `stores/` - Pinia store for state management
  - `api/` - API client configuration
  - `styles/` - Global styles

## Technology Stack

- **Vue.js 3** - Progressive JavaScript framework
- **Vite** - Next generation frontend tooling
- **Vue Router** - Client-side routing
- **Pinia** - State management
