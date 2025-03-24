# 🚗 Ride Sharing API 

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

    1️⃣ Clone the repository
    
        git clone https://github.com/megha-unnikrishnan/ride-sharing-api.git
        
        cd ride-sharing-api

    2️⃣ Create a virtual environment
    
        python -m venv venv
        
        source venv/bin/activate  # On Windows use: venv\Scripts\activate

    3️⃣ Install dependencies
    
        pip install -r requirements.txt

    4️⃣ Apply database migrations
    
        python manage.py migrate

    5️⃣ Start Redis server
    
        redis-server

    6️⃣ Start Celery worker
    
        celery -A ride_sharing_api worker --loglevel=info
        celery -A ridesharing beat --loglevel=info

# 7️⃣ Run the Django server
python manage.py runserver
