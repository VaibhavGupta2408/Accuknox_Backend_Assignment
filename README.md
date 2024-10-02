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
   git clone [<your-repo-url>](https://github.com/VaibhavGupta2408/Accuknox_Backend_Assignment)

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt

4. **Set up PostgreSQL (or any other preferred database):**
   ![image](https://github.com/user-attachments/assets/65842f82-c41d-4f94-a098-245a14b81927)
   - Create a database and update the **DATABASES** setting in **settings.py**.
   - PostgreSQL:
     ```bash
     DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'social_network_db',
           'USER': 'your_db_user',
           'PASSWORD': 'your_db_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
      }


6. **Run database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate

7. **Run Redis (if not already running):**
   ```bash
      redis-server.exe  # On Windows

8. **Run the Django development server:**
   ```bash
      python manage.py runserver

9. **Create a superuser for the admin panel (optional):**
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
  ![image](https://github.com/user-attachments/assets/cefd0c71-9f18-4db7-9962-a81c171c6062)


## User Login
- URL: 
   ```bash 
   /api/users/login/
- Method: POST
- Payload: { "email": "user@example.com", "password": "yourpassword" }
- Response: JWT access and refresh tokens.
  ![image](https://github.com/user-attachments/assets/65379671-3fb0-4bec-b031-c318f118f61c)

## Send Friend Request
- URL: 
   ```bash 
   /api/users/friend-request/send/<receiver_id>/
- Method: POST
- Response: Success or failure message.
  ![image](https://github.com/user-attachments/assets/5b650a43-d4f1-4b56-9c0b-ea3e15d657b9)

## Respond to Friend Request
- URL: 
   ```bash
      /api/users/friend-request/respond/<request_id>/<action>/
- Method: POST
- Actions: Accept or Reject (accept, reject)
- Response: Friend request status update message.
  ![image](https://github.com/user-attachments/assets/4674129d-92dc-4791-af40-c12d61c9f9f2)


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
-- Because there is no friend (In arnav case)
![image](https://github.com/user-attachments/assets/86b6f2cb-1ace-45ff-9d53-8ab001785521)


## Search Users
- URL: 
   ```bash
      /api/users/search/
- Method: GET
- Query Param: search=<keyword>
- Response: List of users matching the search keyword.
  ![image](https://github.com/user-attachments/assets/6bd03a2b-a447-4368-bba7-143ef0c07eeb)


## View User Activities
- URL: 
   ```bash
      /api/users/activity/
- Method: GET
- Response: List of user activities.
  ![image](https://github.com/user-attachments/assets/b4909826-6c78-4598-9fbf-be1d8de99ca4)

## User Logout
- URL:
  ```bash
     /api/users/logout/
- Method: POST
  ![image](https://github.com/user-attachments/assets/cbe3a10c-2509-4c72-8d75-8ce02b52285e)


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
     
   
