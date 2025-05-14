# Nykaa User Dashboard - Full Stack Application

# Overview

This is a full-stack **User Management Dashboard** developed for **Nykaa**, built using **FastAPI** for the backend and **Streamlit** for the frontend. It provides authentication, CRUD operations, session control, and analytics visualizations of user data.

> The goal is to provide a simple yet secure user interface to manage and visualize user activity within the system.

# Features

# Authentication & Security
- Email + Password-based login
- JWT Token Authentication
- Session timeout (5 minutes inactivity)

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
   "D:\DataAnalysisProject\env\fastapi_app\env.local\Screenshot 2025-05-14 195339.png"

2. User Management:
   "D:\DataAnalysisProject\env\fastapi_app\env.local\Screenshot 2025-05-14 195545.png"

3. User Statistics:
   "D:\DataAnalysisProject\env\fastapi_app\env.local\Screenshot 2025-05-14 195614.png"

   






