import streamlit as st
from database import *
from user import authenticate_user, register_user
from pages.Dashboard import dashboard

def login_page():
    email = st.text_input('Email Address', key='login_email_input')
    password = st.text_input('Password', type='password', key='login_password_input')

    if st.button('Login', key='login_button'):
        user = authenticate_user(email, password)
        if user:
            st.session_state['user_authenticated'] = True
            st.success('Welcome back!')
            st.experimental_rerun()
        else:
            st.error('Invalid email or password. Please try again.')

def signup_page():
    email = st.text_input('Email Address', key='signup_email_input')
    password = st.text_input('Password', type='password', key='signup_password_input')

    if st.button('Sign Up', key='signup_button'):
        existing_user = authenticate_user(email, password)
        if existing_user:
            st.error('An account with this email already exists.')
        else:
            register_user(email, password)
            st.success('Account created successfully. You can now login.')
            login_page()

def app():
    if 'user_authenticated' not in st.session_state:
        st.session_state['user_authenticated'] = False

    st.title('Welcome to Forcastock')
    choice = st.radio('Login/Signup', ['Login','Sign Up'], key='login_signup_radiobutton')

    if choice == 'Login':
        login_page()  # Show the login page
    else:
        signup_page()  # Show the signup page

    st.sidebar.title('Navigation')

    if st.session_state.user_authenticated:
        # Allow access to pages if user is authenticated
        page = st.sidebar.radio('Go to', ['Dashboard', 'Settings'])

        if page == 'Dashboard':
            st.empty()
            dashboard()
        elif page == 'Settings':
            st.write('Settings page content...')
    else:
        # Redirect to login page if user is not authenticated
        st.sidebar.write('Please login to access the navigation')

if __name__ == "__main__":
    app()
