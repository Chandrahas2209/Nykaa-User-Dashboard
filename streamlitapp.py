import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
# Set FastAPI backend URL
API_URL = "http://localhost:8000"
# Session duration set to 10 minutes
SESSION_DURATION = 10 * 60  # seconds
# Configure the Streamlit page
st.set_page_config(page_title="Nykka User Dashboard", layout="wide")
# Initialize Streamlit session state variables
if "access_token" not in st.session_state:
    st.session_state.access_token = None
if "email" not in st.session_state:
    st.session_state.email = ""
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "session_start_time" not in st.session_state:
    st.session_state.session_start_time = None
if "page" not in st.session_state:
    st.session_state.page = "Users CRUD"
# Logout function to clear session state and rerun
def logout():
    st.session_state.logged_in = False
    st.session_state.access_token = None
    st.session_state.email = ""
    st.session_state.session_start_time = None
    st.success("Logged out successfully.")
    st.rerun()
# Session timer to auto logout after session duration
def session_timer():
    if st.session_state.session_start_time:
        elapsed = (datetime.now() - st.session_state.session_start_time).total_seconds()
        remaining = SESSION_DURATION - elapsed
        if remaining <= 0:
            st.warning("Session expired. Logging out...")
            logout()
        else:
            mins, secs = divmod(int(remaining), 60)
            st.sidebar.markdown(f"⏳ **Session Time Left:** {mins:02}:{secs:02}")
# Login form to authenticate user
def login_form():
    st.title(" Nykka User Dashboard Login") # Title for login
    email = st.text_input("Email") # Email input
    password = st.text_input("Password", type="password")  # Password input

    if st.button("Login"):  # Submit login form
        if not email or not password:
            st.warning("Please fill in all fields.")
        else:
            payload = {"email": email, "password": password}
            try:
                response = requests.post(
                    f"{API_URL}/token",
                    data=payload,
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                # Successful login
                if response.status_code == 200:
                    st.session_state.access_token = response.json().get("access_token", "")
                    st.session_state.email = email
                    st.session_state.logged_in = True
                    st.session_state.session_start_time = datetime.now()
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error(f"Login failed: {response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"Exception occurred: {e}")
# Sidebar navigation and session timer display
def navigation_bar():
    session_timer()
    st.sidebar.title(" Dashboard Menu")
    st.sidebar.write(f"👤 Logged in as: `{st.session_state.email}`")
    st.session_state.page = st.sidebar.radio("Navigate to:", ["Users CRUD", "User Graphs", "Logout"])
# Main dashboard function after login
def dashboard():
    navigation_bar()
    headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
    # Fetch user list from backend
    users = []
    try:
        response = requests.get(f"{API_URL}/users/", headers=headers)
        if response.status_code == 200:
            users = response.json()
        elif response.status_code == 401:
            logout()
        else:
            st.error(f"Failed to fetch users: {response.json()}")
    except Exception as e:
        st.error(f"Error fetching users: {e}")

    page = st.session_state.page
    # Users CRUD Tabbed Layout
    if page == "Users CRUD":
        st.title(" User Management")
        tab1, tab2, tab3, tab4 = st.tabs([" Create", " Read", " Update", " Delete"])
        # Create user form
        with tab1:
            st.subheader("Create User")
            name = st.text_input("Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            if st.button("Create"):
                if not name or not email or not password:
                    st.warning("Please fill in all fields.")
                elif any(user["email"] == email for user in users):
                    st.warning(" User with this email already exists.")
                else:
                    data = {"name": name, "email": email, "password": password}
                    try:
                        res = requests.post(f"{API_URL}/users/", json=data, headers=headers)
                        if res.status_code in [200, 201]:
                            st.success(" User created successfully!")
                            st.rerun()
                        else:
                            st.error(f"Error: {res.json().get('detail', 'Unknown error')}")
                    except Exception as e:
                        st.error(f"Exception occurred: {e}")
        # Display list of users in a table
        with tab2:
            st.subheader("All Users")
            if users:
                try:
                    df = pd.DataFrame(users)
                    df["created_at"] = pd.to_datetime(df["created_at"])
                    df = df.sort_values("created_at", ascending=False)
                    if "password" in df.columns:
                        df = df.drop(columns=["password"]) # Hide password
                    st.dataframe(df, use_container_width=True)
                except Exception as e:
                    st.error(f"Error displaying users: {e}")
            else:
                st.info("No users found.")
        # Update user form
        with tab3:
            st.subheader("Update User")
            user_options = {f"{user['name']} ({user['email']})": user for user in users}
            selected = st.selectbox("Select user to update", list(user_options.keys()))

            if selected:
                selected_user = user_options[selected]
                new_name = st.text_input("New Name", value=selected_user["name"])
                new_email = st.text_input("New Email", value=selected_user["email"])
                new_password = st.text_input("New Password", type="password")

                if st.button("Update"):
                    if not new_name or not new_email or not new_password:
                        st.warning("Please fill in all fields.")
                    else:
                        data = {"name": new_name, "email": new_email, "password": new_password}
                        try:
                            res = requests.put(
                                f"{API_URL}/users/{selected_user['id']}", json=data, headers=headers
                            )
                            if res.status_code == 200:
                                st.success(" User updated successfully!")
                                st.rerun()
                            else:
                                st.error(f"Update failed: {res.json().get('detail', 'Unknown error')}")
                        except Exception as e:
                            st.error(f"Exception occurred: {e}")
       # Delete user
        with tab4:
            st.subheader("Delete User")
            del_selected = st.selectbox("Select user to delete", list(user_options.keys()))

            if del_selected:
                del_user = user_options[del_selected]
                if st.button("Delete"):
                    try:
                        res = requests.delete(f"{API_URL}/users/{del_user['id']}", headers=headers)
                        if res.status_code == 200:
                            st.success(" User deleted successfully!")
                            st.rerun()
                        else:
                            st.error(f"Delete failed: {res.json().get('detail', 'Unknown error')}")
                    except Exception as e:
                        st.error(f"Exception occurred: {e}")
   # User Graph Visualization
    elif page == "User Graphs":
        st.title(" User Statistics")
        if users:
            df = pd.DataFrame(users)
            df["created_at"] = pd.to_datetime(df["created_at"])
            df["date"] = df["created_at"].dt.date
            daily_count = df.groupby("date").size().reset_index(name="count")
            # Show metrics
            col1, col2 = st.columns(2)
            with col1:
                st.metric("👥 Total Users", len(users))
            with col2:
                st.metric(" Latest Joined", df["created_at"].max().strftime("%Y-%m-%d %H:%M:%S"))
           # Bar graph of daily user registrations
            st.plotly_chart(px.bar(daily_count, x="date", y="count", title="User Registrations Over Time"), use_container_width=True)
        else:
            st.info("No users available for graph.")
    # Logout handler
    elif page == "Logout":
        logout()

# Entry point – checks login state
if st.session_state.logged_in:
    dashboard()
else:
    login_form()
