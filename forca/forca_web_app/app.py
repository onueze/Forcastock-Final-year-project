import streamlit as st
from database import *
from user import authenticate_user, register_user
# Importing other pages
from pages.Dashboard import display_dashboard

def login_page():
    email = st.text_input('Email Address', key='login_email_input')
    password = st.text_input('Password', type='password', key='login_password_input')

    if st.button('Login', key='login_button'):
        user = authenticate_user(email, password)
        if user:
            st.session_state['user_authenticated'] = True
            st.session_state['current_page'] = 'dashboard'  # Direct user to dashboard after login
            st.rerun()  # Rerun the app to reflect the session state change
        else:
            st.error('Invalid email or password. Please try again.')

def signup_page():
    st.subheader('Sign Up')
    email = st.text_input('Email Address', key='signup_email_input')
    password = st.text_input('Password', type='password', key='signup_password_input')

    if st.button('Sign Up', key='signup_button'):
        existing_user = authenticate_user(email, password)
        if existing_user:
            st.error('An account with this email already exists.')
        else:
            register_user(email, password)
            st.success('Account created successfully. You can now login.')

def app():
    st.title('Welcome to Forcastock')
    if 'user_authenticated' not in st.session_state:
        st.session_state['user_authenticated'] = False

    if not st.session_state['user_authenticated']:
        choice = st.radio('Login/Signup', ['Login', 'Sign Up'])
        if choice == 'Login':
            login_page()
        else:
            signup_page()
    else:
        # Navigation for authenticated users
        if 'current_page' not in st.session_state:
            print('set')
            st.session_state['current_page'] = 'dashboard'  # 'Home' page

        if st.session_state['current_page'] == 'dashboard':
            
            display_dashboard()  # Display dashboard
