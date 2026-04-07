# NotifyHub - Real-Time Notification & Activity Feed System

NotifyHub is a comprehensive Django-based platform designed for modern social interactions. It features a real-time notification engine, a personalized activity feed, and a detailed user engagement system.

## Key Features

### 1. Real-Time Interactions
- WebSocket-Powered Alerts: Delivery of notifications using Django Channels and Daphne.
- Dynamic Unread Count: Real-time updates to the notification bell in the navbar, ensuring users stay informed without page refreshes.

### 2. Social Ecosystem
- Personalized Activity Feed: A custom feed engine that aggregates posts and actions relevant to the logged-in user.
- User Profiles & Follow System: Full social graph support with follow/unfollow capabilities and dedicated profile views.
- Rich Posting & Comments: Create, view, and interact with posts and multi-threaded comments.
- Mention System: Advanced @username detection using regex to tag and notify specific users within discussions.

### 3. Technical Architecture
- Generic Notification Engine: Built using Django's ContentType framework to link notifications with any object (Posts, Comments, Profiles).
- Automated Triggers: Decoupled event lifecycle with Django signals, ensuring system-wide notification consistency.
- Scalable Design: Prepared for high-volume traffic with a modular schema.

---

## How to Run the System

### Prerequisites
- Python 3.x
- Django 4.x

### Setup Steps

1. Clone or Navigate to the Directory
   ```bash
   cd notification-activity-system-main
   ```

2. Install Dependencies
   Ensure you have pip installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. Database Initialization
   Apply the migrations to set up your database schema:
   ```bash
   cd notification-activity-system-main
   python manage.py migrate
   ```

4. Seed the Database
   Populate the database with the required notification categories (like follows, comments, and mentions):
   ```bash
   python seed.py
   ```

5. Launch the Development Server
   Run the project using the development server:
   ```bash
   python manage.py runserver
   ```

5. Access the System
   Open your browser and navigate to: http://127.0.0.1:8000/
