# send_reminders.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import psycopg2
import os
from dotenv import load_dotenv

# This email scheduler is executed within a different folder on the developers device due to access problems but still included into the submitted repository
def fetch_inactive_users():
    """Fetch users who made a trade between 0 to 12 hours ago."""
    
    # Get database connection parameters from environment variables. The environment variables are not pushed to the github repo for safety
    db_name = os.environ.get('DB_NAME')
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    db_host = os.environ.get('DB_HOST')
    db_port = os.environ.get('DB_PORT')
    
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        cur = conn.cursor()

        # This query fetches emails of users who have a transaction timestamp 
        # between 24 to 48 hours ago but no transactions in the last 24 hours.
        cur.execute("""
        SELECT DISTINCT u.email
        FROM users u
        INNER JOIN demo_accounts da ON u.id = da.user_id
        INNER JOIN transactions t ON da.demo_id = t.demo_id
        WHERE t.timestamp BETWEEN NOW() - INTERVAL '48 hours' AND NOW() - INTERVAL '24 hours'
        AND u.id NOT IN (
            SELECT da.user_id
            FROM demo_accounts da
            INNER JOIN transactions t ON da.demo_id = t.demo_id
            WHERE t.timestamp > NOW() - INTERVAL '24 hours'
        );
        """)

        users = cur.fetchall()
        cur.close()
        return [email[0] for email in users]
    except Exception as e:
        print(f"Database query failed: {e}")
        return []
    finally:
        if conn:
            conn.close()


 # REUSED CODE FOR SENDING EMAILS LINE 49-75 https://python.readthedocs.io/fr/hack-in-language/library/email-examples.html
def send_email(to_address):
    """Send a reminder email to the specified address."""
    
    smtp_server = os.environ.get('SMTP_SERVER')
    smtp_port = int(os.environ.get('SMTP_PORT'))  # Convert port to integer
    smtp_user = os.environ.get('SMTP_USER')
    smtp_password = os.environ.get('SMTP_PASSWORD')
    

    # Setup message
    body = "Hi there, don't forget to place your trade today to keep up with your trading goals!\n\nYour Forcastock Team"
    message = MIMEMultipart()
    message.attach(MIMEText(body, 'plain'))
    message['Subject'] = 'Forcastock Reminder: Time to Place Your Next Trade'
    message['From'] = smtp_user
    message['To'] = to_address

    # Send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        # Secure the connection
        server.starttls()  
        # Login to the SMTP server
        server.login(smtp_user, smtp_password)  
        server.sendmail(smtp_user, to_address, message.as_string())
    except Exception as e:
        print(f"Error sending verification email: {e}")
    finally:
        server.quit()  # Terminate the SMTP session



inactive_users = fetch_inactive_users()
for user_email in inactive_users:
    send_email(user_email)
    print(f"Sent reminder to {user_email}")


