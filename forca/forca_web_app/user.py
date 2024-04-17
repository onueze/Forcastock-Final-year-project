from database import *


def authenticate_user(email):
    """
    User email attempting to log in is checked against the database
    """
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            # Check if the user with the given email and password exists in the database
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            if user:
                # If a user is found, return a dictionary wisth user details
                return {'id': user[0], 'email': user[1]}
            else:
                return None
            
        except psycopg2.Error as e:
            print("Error executing SQL query:", e)
            return None
    else:
        return None
    
def register_user(email):
    """
    User email will be registered
    """
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            # Check if the user with the given email already exists
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                print("User with this email already exists.")
            else:
                # Insert the new user into the database
                insert_query = "INSERT INTO users (email) VALUES (%s)"
                cursor.execute(insert_query, (email,))
                conn.commit()
                print("User registered successfully.")
            
            cursor.close()
            conn.close()
        except psycopg2.Error as e:
            print("Error executing SQL query:", e)
    else:
        print("Error connecting to the database.")