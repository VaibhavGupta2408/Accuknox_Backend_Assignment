# Social Networking API Project

This project is a backend for a social networking application, featuring user management, friend requests, user activities, and more. It is built using Django and Django REST Framework.

## Features:
- User signup and login with JWT authentication.
- Friend request system.
- User activity logging.
- Redis caching for optimized performance.
- API endpoints for searching users and managing friend requests.

## Installation Steps

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt

4. **Set up PostgreSQL (or any other preferred database):**
   - Create a database and update the **DATABASES** setting in **settings.py**.
   - PostgreSQL:
     ```bash
     DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_db_name',
           'USER': 'your_db_user',
           'PASSWORD': 'your_db_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
      }

5. **Run database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate

6. **Run Redis (if not already running):**
   ```bash
      redis-server.exe  # On Windows

7. **Run the Django development server:**
   ```bash
      python manage.py runserver

8. **Create a superuser for the admin panel (optional):**
   ```bash
      python manage.py createsuperuser

# API Documentation

## User Signup
- URL: 
   ```bash 
   /api/users/signup/
- Method: POST
- Payload: { "email": "user@example.com", "password": "yourpassword" }
- Response: User creation success message.

## User Login
- URL: 
   ```bash 
   /api/users/login/
- Method: POST
- Payload: { "email": "user@example.com", "password": "yourpassword" }
- Response: JWT access and refresh tokens.

## Send Friend Request
- URL: 
   ```bash 
   /api/users/friend-request/send/<receiver_id>/
- Method: POST
- Response: Success or failure message.

## Respond to Friend Request
- URL: 
   ```bash
      /api/users/friend-request/respond/<request_id>/<action>/
- Method: POST
- Actions: Accept or Reject (accept, reject)
- Response: Friend request status update message.

## View Friends List
- **URL:** `/api/users/friends/`
- **Method:** GET
- **Response:** List of user's friends.
  ```json
  [
    {
      "id": 1,
      "email": "friend@example.com",
      "username": "friend1",
      "status": "Accepted"
    }
  ]

## Search Users
- URL: 
   ```bash
      /api/users/search/
- Method: GET
- Query Param: search=<keyword>
- Response: List of users matching the search keyword.

## View User Activities
- URL: 
   ```bash
      /api/users/activity/
- Method: GET
- Response: List of user activities.


# Postman Collection
- Download the Postman Collection

# Requirements

- Python 3.x
- Django
- Django REST Framework
- djangorestframework-simplejwt
- psycopg2
- Redis

# Dependencies:
- All dependencies are listed in **requirements.txt**.
     
   
