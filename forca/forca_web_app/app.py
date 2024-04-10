import streamlit as st
from database import *
from user import authenticate_user, register_user
from About import about_page

import random
import smtplib
from email.mime.text import MIMEText

import time
# Importing other pages

#from pages.Dashboard import display_dashboard
#from pages.StockPrediction import show_stock_prediction
#from pages.DemoTrading import show_demo_trading


import smtplib
from email.mime.text import MIMEText

choice = None
 # REUSED CODE FOR SENDING EMAILS LINE 22-47 https://python.readthedocs.io/fr/hack-in-language/library/email-examples.html
def send_verification_email(user_email, verification_code):
    smtp_server = 'smtp.gmail.com'  
    smtp_port = 587  # commonly 587 for TLS
    smtp_user = 'forcastocks@gmail.com'  
    smtp_password = 'kjwx djbc bgno ssan'  

    # Setup message
    message = MIMEText(f"Your verification code is: {verification_code}")
    message['Subject'] = 'Your Forcastock Verification Code'
    message['From'] = smtp_user
    message['To'] = user_email

    # Send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        # Secure the connection
        server.starttls()  
        # Login to the SMTP server
        server.login(smtp_user, smtp_password)  
        server.sendmail(smtp_user, user_email, message.as_string())
        print(f"Verification code sent to {user_email}")
    except Exception as e:
        print(f"Error sending verification email: {e}")
    finally:
        server.quit()  # Terminate the SMTP session


def generate_verification_code():
    return random.randint(100000, 999999)

def login_page():
    
    st.subheader('Login')
    email = st.text_input('Email Address', key='login_email_key')

    if 'verification_sent' not in st.session_state:
        st.session_state.verification_sent = False

    if st.button('Send Verification Code', key='send_verification_button'):
        user = authenticate_user(email)
        if user:
            verification_code = generate_verification_code()
            send_verification_email(email, verification_code)
            st.session_state['verification_sent'] = True
            st.session_state['verification_code'] = verification_code
            placeholder = st.empty()

            # Show a message
            placeholder.info('Verification code sent. Please check your email.')

            # Wait for 5 seconds
            time.sleep(5)

            # Clear the message
            placeholder.empty()
        else:
            st.error('Email not found. Please sign up or try again.')

    if st.session_state.verification_sent:
        entered_code = st.text_input('Verification Code', key='verification_code_input')
        if st.button('Verify & Login', key='verify_login_button'):
            if 'verification_code' in st.session_state and int(entered_code) == st.session_state['verification_code']:
                # User is authenticated successfully
                user = authenticate_user(email)
                st.session_state['user_authenticated'] = True
                st.session_state['user_id'] = user['id']
                st.session_state['user_email'] = user['email']  
                st.session_state['current_page'] = 'about'  
                st.session_state['verification_sent'] = False
                del st.session_state['verification_sent']  # Cleanup
                del st.session_state['verification_code']
                st.rerun()
            
            else:
                st.error('Invalid verification code. Please try again.')


def signup_page():
    st.subheader('Sign Up')
    email = st.text_input('Email Address', key='signup_email_input')
    
    if 'verification_sent' not in st.session_state:
        st.session_state.verification_sent = False

    # This button will trigger the verification process
    if st.button('Send Verification Code', key='verify_button'):
        # Check if the user already exists
        existing_user = authenticate_user(email)
        if existing_user:
            st.error('An account with this email already exists.')
        else:
            # User does not exist, send a verification code
            verification_code = generate_verification_code()
            send_verification_email(email, verification_code)
            st.session_state['verification_sent'] = True
            st.session_state['verification_email'] = email  # Store the email in session state
            st.session_state['verification_code'] = verification_code  # Store the code in session state
            st.info('Verification code sent. Please check your email.')
            
            
    if st.session_state.verification_sent:
        # User will enter the verification code they received
        user_code_input = st.text_input('Enter Verification Code', key='user_code_input')
    
        # Check if the entered code matches the sent code
        if st.button('Verify Email', key='verify_email_button'):
            if 'verification_code' in st.session_state and int(user_code_input) == st.session_state['verification_code']:
                # Email is verified, proceed with registration
                register_user(st.session_state['verification_email'])
                st.session_state['current_page'] = 'login'
                # Clean up email from session state
                del st.session_state['verification_email']  
                # Clean up code from session state
                del st.session_state['verification_code']
                st.success('Account created successfully. You can now login.')
                
            else:
                st.error('Incorrect verification code.')

def app():
    st.title('Welcome to Forcastock')
    if 'user_authenticated' not in st.session_state:
        st.session_state['user_authenticated'] = False
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = ''  # Default page

    # Main app logic
    if not st.session_state['user_authenticated']:
        # Initialize 'choice' in session state if not present
        if 'choice' not in st.session_state:
            st.session_state['choice'] = 'Login'

        # The radio widget directly updates 'choice' in session_state
        choice = st.radio('Login/Signup', ['Login', 'Sign Up'], key='choice')

        if choice == 'Login':
            login_page()
        elif choice == 'Sign Up':
            signup_page()
    else:
        about_page()
         
            
        
