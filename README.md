# Nykaa User Dashboard - Full Stack Application

# Overview

This is a full-stack **User Management Dashboard** developed for **Nykaa**, built using **FastAPI** for the backend and **Streamlit** for the frontend. It provides authentication, CRUD operations, session control, and analytics visualizations of user data.

> The goal is to provide a simple yet secure user interface to manage and visualize user activity within the system.

# Features

# Authentication & Security
- Email + Password-based login
- JWT Token Authentication
- Session timeout (10 minutes inactivity)

# User Management (CRUD)
- Create, Read, Update, Delete (CRUD) operations for users
- Duplicate user email validation
- Feedback alerts on all operations

# Analytics Dashboard
- Real-time metrics:
  - Total number of users
  - Most recent user signup
- Interactive bar chart of daily user registrations using Plotly

# Session Handling
- Auto-logout after inactivity
- Session timer displayed in sidebar

# Tech Stack

| Layer       | Technology Used |
|-------------|-----------------|
| **Frontend**| Streamlit, Plotly |
| **Backend** | FastAPI, Pydantic |
| **Database**| SQLite (can be switched to PostgreSQL/MySQL) |
| **Other**   | Python, JWT for Auth, Requests, Pandas |

---

# Project Structure
- ├── backend/
- │ ├── main.py # FastAPI application with auth & CRUD
- │ ├── models.py # Pydantic models
- │ ├── database.py # SQLite database setup
- │ └── utils.py # JWT helper functions
- ├── frontend/
- │ └── app.py # Streamlit dashboard
- ├── README.md
- └── requirements.txt

# Installation & Setup

1. Clone the repository
   ```bash
   git clone https://github.com/your-username/nykaa-user-dashboard.git
   cd nykaa-user-dashboard
   
2. Create a virtual environment:
   - python -m venv venv
   - source venv/bin/activate  # On Windows: venv\Scripts\activate
   
3. Install dependencies:
   - pip install -r requirements.txt
   
4. Run the backend (FastAPI):
   - cd backend
   - uvicorn main:app --reload
   
5. Run the frontend (Streamlit):
   - cd frontend
   - streamlit run app.py

# Demo Screenshots

1. Login Screen:
   
   ![Screenshot 2025-05-14 195339](https://github.com/user-attachments/assets/73dc00ce-b647-4923-80c2-b2e51b1b0d7d)


3. User Management:
   
   ![Screenshot 2025-05-14 195545](https://github.com/user-attachments/assets/f0e1b625-587e-42d8-bc37-8f4711bb3aca)


5. User Statistics:
   
   ![Screenshot 2025-05-14 195614](https://github.com/user-attachments/assets/4fabde2e-e36e-4974-9341-b3918ca463b1)


# Why These Tools?:
 - Why FastAPI?
   - Fast, modern, async-ready API development
   - Built-in Swagger documentation
   - Easy JWT integration and schema validation
     
 - Why Streamlit?
   - Quick prototyping and deployment
   - Simplified UI without the need for HTML/CSS/JS
   - Perfect for dashboard-based apps
   
 - Alternatives:
   - Frontend: React.js + Flask API (more scalable but more complex)
   - Backend: Django REST Framework (heavier, more suitable for larger projects)

# Future Improvements
 - Integrate PostgreSQL or MongoDB for production
 - Dockerize app for containerized deployment
 - Add role-based access (admin/user)
 - Add email verification and password recovery

# Credits
- Developed by Mallipeddi Chandrahas



   






