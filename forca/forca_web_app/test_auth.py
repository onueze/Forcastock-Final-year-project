from streamlit.testing.v1 import AppTest


def test_login_functionality():
    at = AppTest.from_file("Landing.py")
    
    # Initialize the app
    at.run()
    
    # Select the 'Login' option
    at.radio("Login/Signup").select("Login")
    
    # Fill the login form
    at.text_input("Email Address", key='login_email_input').input("valid_email@example.com")
    at.text_input("Password", key='login_password_input').input("valid_password")
    
    # Click the login button
    at.button("Login").click()

    # Run the app after interacting
    at.run()

    # Verify successful login
    assert "Logged in successfully" in at.text



def test_signup_functionality():
    at = AppTest.from_file("Landing.py")
    
    # Initialize the app
    at.run()
    
    # Select the 'Sign Up' option
    at.radio("Login/Signup").select("Sign Up")
    
    # Fill the signup form
    at.text_input("Email Address", key='signup_email_input').input("new_user@example.com")
    at.text_input("Password", key='signup_password_input').input("new_password")
    
    # Click the signup button
    at.button("Sign Up").click()

    # Run the app after interacting
    at.run()

    # Verify successful signup
    assert "Account created successfully" in at.text

