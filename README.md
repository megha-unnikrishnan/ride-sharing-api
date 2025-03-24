

## 📌 Introduction

    This document provides a detailed overview of the Ride Sharing API built with Django Rest Framework (DRF). The API supports:

        ✔️ User authentication (registration, login)
        
        ✔️ Ride management (CRUD operations for rides)
        
        ✔️ Ride status updates (Requested, Matched, Accepted, Started, Completed, Cancelled)
        
        ✔️ Ride matching (algorithm for assigning rides to drivers)
        
        ✔️ Real-time ride tracking using Celery & Redis
        
        ✔️ Asynchronous task handling using Celery

## 🎯 Features

### 🚀 User API

      ✔️ User registration & login using Django Rest Framework (DRF) & JWT.

      ✔️ User roles: Riders & Drivers.

### 🚖 Ride API

      ✔️ Create, Read, Update, Delete (CRUD) operations for rides.

      ✔️ View ride details.

      ✔️ List all rides.

### 🔄 Ride Status Updates

      ✔️ Update ride status: Requested → Matched → Accepted → Started → Completed / Cancelled.

### 🏎 Ride Matching 

      ✔️ Algorithm for matching riders with available drivers.

      ✔️ Drivers can accept ride requests via API.

### 📍 Real-time Ride Tracking 

      ✔️ Simulated updates for ride location tracking.

### ✅ Testing

      ✔️ Basic Django tests for models and API endpoints.

## ⚙️ Installation & Setup

### 📌 Prerequisites

    ✔️ Ensure you have the following installed:

  - Python 3.x

  - Django

  - Django Rest Framework (DRF)

  - Celery

  - Redis (for task queue management)

  - djangorestframework-simplejwt (For JWT authentication)

### 🛠️ Setup Instructions

    ✔️ Clone the repository
    
        git clone https://github.com/megha-unnikrishnan/ride-sharing-api.git
        
        cd ride-sharing-api

    ✔️ Create a virtual environment
    
        python -m venv venv
        
        source venv/bin/activate  # On Windows use: venv\Scripts\activate

    ✔️ Install dependencies
    
        pip install -r requirements.txt

    ✔️ Apply database migrations
    
        python manage.py migrate

    ✔️ Start Redis server
    
        redis-server

    ✔️ Start Celery worker
    
        celery -A ride_sharing_api worker --loglevel=info

    ✔️ Start Celery beat
        
        celery -A ridesharing beat --loglevel=info

    ✔️ Run the Django server
    
        python manage.py runserver

## 👮 User API

### 📁 User Model

### 🌐 API Endpoints  

| Method | Endpoint               | Description            |
|--------|------------------------|------------------------|
| POST   | `/users/register/` | Register a new user   |
| POST   | `/users/login/`    | Login & get JWT token |

For driver:

    Registration:

![Image](https://github.com/user-attachments/assets/3628ee61-0a25-449e-9e97-298749b8ba7e)

    Login:

![Image](https://github.com/user-attachments/assets/fb3b0653-02ec-44b0-abbd-81a70ddacebe)


For Rider:

    Registration:

![Image](https://github.com/user-attachments/assets/dffadb72-d6a3-4305-9cba-f21e0768e8a9)

    Login:

![Image](https://github.com/user-attachments/assets/42d23429-d968-475f-8c1f-62e5217c0609)


## 🚖 Ride API

### 🌐 Ride API Endpoints  

| Method | Endpoint                     | Description            |
|--------|------------------------------|------------------------|
| POST   | `/api/rides/`                | Create a new ride     |
| GET    | `/api/rides/{ride_id}/`      | View ride details     |
| PATCH  | `/api/rides/{ride_id}/status/` | Update ride status    |


Create a ride:

![Image](https://github.com/user-attachments/assets/151e106e-3dee-4758-a1fb-8a141502e73f)

Get ride details:

![Image](https://github.com/user-attachments/assets/02225b3d-b6ad-4e7a-a460-33ba76662d3e)

Update Ride details:

![Image](https://github.com/user-attachments/assets/8c8c0c47-ef71-4327-94d1-efe6c1003361)

## 🚗 Ride Matching 

### 🛠️ Matching Algorithm

- Find the first available driver.

- Assign the ride to the driver.

- Update the ride status to Matched.

Available driver:

![Image](https://github.com/user-attachments/assets/692ad610-e006-4b8e-a70c-2a289e7aaa14)

Update the ride status to matched:

![Image](https://github.com/user-attachments/assets/0a2e26ae-3be5-4c70-8fef-e52f5b4d9b55)

Driver accepts the ride:

![Image](https://github.com/user-attachments/assets/cfca8f6c-9089-4661-af47-1470d1274571)

Update the ride status to accepted:

![Image](https://github.com/user-attachments/assets/cd2d906a-bbf3-4b6c-8bb1-4d1399f96da2)

