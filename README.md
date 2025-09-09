
🚀 IEC API

A backend API built with Django REST Framework, deployed on PythonAnywhere, for managing authentication, payments, and API endpoints.
This project is part of the IEC Internship Project.

🌍 Live API

Base URL: https://iecapi.pythonanywhere.com/api

🔗 API Endpoints

Authentication

Register a new user → POST /api/register/

Obtain JWT token (for frontend login) → /api/token/

Refresh JWT token → POST /api/token/refresh/

Example usage:

{
  "username": "your_username",
  "password": "your_password"
}


API Documentation

Swagger UI → /api/docs/

ReDoc → /api/redoc/

OpenAPI Schema (JSON) → /api/schema/

Payments

Stripe integration with test keys

Create checkout sessions via /api/payments/create-checkout-session/

⚡ Features

Authentication (JWT + Django session auth)

Custom User model

Stripe Payment Gateway integration

CORS support for frontend integration

Interactive API docs (Swagger + Redoc)

Deployed on PythonAnywhere

🛠️ Tech Stack

Backend: Django 5, Django REST Framework

Auth: JWT (via djangorestframework-simplejwt)

Payments: Stripe

Docs: drf-spectacular (Swagger, ReDoc)

Hosting: PythonAnywhere

📂 Project Structure
iecapi/
│── api/            # Core API app (auth, users, endpoints)
│── payments/       # Stripe payment logic
│── iecapi/         # Project config (settings, urls, wsgi, asgi)
│── staticfiles/    # Collected static files
│── media/          # Media uploads
│── .env            # Environment variables (not pushed to GitHub)

⚙️ Environment Variables (.env)

Create a .env file in your project root:

# Django
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=iecapi.pythonanywhere.com,127.0.0.1,localhost

# Stripe
STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxxxxxxxxxxx
STRIPE_PUBLISHABLE_KEY=pk_test_xxxxxxxxxxxxxxxxxxxxx

🚀 Deployment (PythonAnywhere)

Clone repo on PythonAnywhere

Create virtual environment & install requirements:

pip install -r requirements.txt


Configure WSGI file (/var/www/iecapi_pythonanywhere_com_wsgi.py)

Run migrations:

python manage.py migrate


Collect static files:

python manage.py collectstatic


Reload PythonAnywhere web app 🎉

📖 API Docs Preview

Swagger UI

ReDoc

OpenAPI JSON


👨‍💻 Author

Muhammad Mohtasham Ahmad


Focus: Backend Development (Django + DRF + APIs)

also you can use admin logins to access admin panel and also can generate access token by using admin details. Below is url to admin page and logins.
URL : https://iecapi.pythonanywhere.com/admin
Username ; Owner
Password : owner1122

✨ This API is now live and production-ready on PythonAnywhere!
