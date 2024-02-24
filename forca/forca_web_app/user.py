from database import *


def authenticate_user(email, password):
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            # Check if the user with the given email and password exists in the database
            query = "SELECT * FROM users WHERE email = %s AND password = %s"
            cursor.execute(query, (email, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            return user
        except psycopg2.Error as e:
            print("Error executing SQL query:", e)
            return None
    else:
        return None
    
def register_user(email, password):
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
                insert_query = "INSERT INTO users (email, password) VALUES (%s, %s)"
                cursor.execute(insert_query, (email, password))
                conn.commit()
                print("User registered successfully.")
            
            cursor.close()
            conn.close()
        except psycopg2.Error as e:
            print("Error executing SQL query:", e)
    else:
        print("Error connecting to the database.")