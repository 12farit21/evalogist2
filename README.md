# Cloud ERP (Django Project)

Cloud ERP is a web-based enterprise resource planning (ERP) system built using Django. It includes an admin panel for managing business operations and uses SQLite3 as the database.

## Features
- User authentication and role-based access
- Admin panel for managing users, products, and orders
- Database powered by SQLite3

## Prerequisites
Before running the project, ensure you have the following installed:
- Python 3.8+
- virtualenv 

## Installation & Setup

### 1. Clone the Repository
```sh
git clone https://github.com/12farit21/evalogist2.git
cd cloud-erp
```

### 2. Create a Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Apply Database Migrations
```sh
python manage.py migrate
```

### 5. Create a Superuser (for Admin Panel)
```sh
python manage.py createsuperuser
```
Follow the prompts to set up the admin user.

### 6. Run the Development Server
```sh
python manage.py runserver
```
The application will be available at `http://127.0.0.1:8000/`

## Usage
- Access the admin panel at `http://127.0.0.1:8000/admin/` using the superuser credentials.
- Manage users, products, and other resources from the admin dashboard.

## Deployment
For production deployment, consider using:
- Gunicorn + Nginx for serving the application
- PostgreSQL or MongoDB instead of SQLite3
