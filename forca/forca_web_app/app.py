import streamlit as st
from database import *
from user import authenticate_user, register_user
from About import about_page
# Importing other pages

#from pages.Dashboard import display_dashboard
#from pages.StockPrediction import show_stock_prediction
#from pages.DemoTrading import show_demo_trading

def login_page():
    st.subheader('Login')
    email = st.text_input('Email Address', key='login_email_input')
    password = st.text_input('Password', type='password', key='login_password_input')

    if st.button('Login', key='login_button'):
        user = authenticate_user(email, password)
        if user:
            # User is authenticated successfully
            st.session_state['user_authenticated'] = True
            st.session_state['user_id'] = user['id']  # Access and store the user's ID
            st.session_state['user_email'] = user['email']  # Access and store the user's email
            st.session_state['current_page'] = 'about'  # Direct user to dashboard after login
            st.success(f"Logged in successfully as {user['email']}")
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
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 'login'  # Default page

    if not st.session_state['user_authenticated']:
        choice = st.radio('Login/Signup', ['Login', 'Sign Up'])
        if choice == 'Login':
            login_page()
        else:
            signup_page()
        
    else:    
        about_page()
            
        
