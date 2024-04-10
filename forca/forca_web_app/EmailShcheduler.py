# send_reminders.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import psycopg2
import os


def fetch_inactive_users():
    """Fetch users who made a trade between 0 to 12 hours ago."""
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="Alexel01",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()

        # This query fetches emails of users who have a transaction timestamp 
        # between 0 to 12 hours ago.
        cur.execute("""
        SELECT DISTINCT u.email
        FROM users u
        INNER JOIN demo_accounts da ON u.id = da.user_id
        INNER JOIN transactions t ON da.demo_id = t.demo_id
        WHERE t.timestamp BETWEEN NOW() - INTERVAL '12 hours' AND NOW()
        AND u.id NOT IN (
            SELECT da.user_id
            FROM demo_accounts da
            INNER JOIN transactions t ON da.demo_id = t.demo_id
            WHERE t.timestamp > NOW() - INTERVAL '0 hours'
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
    smtp_server = 'smtp.gmail.com'  
    smtp_port = 587  # commonly 587 for TLS
    smtp_user = 'forcastocks@gmail.com'  
    smtp_password = 'kjwx djbc bgno ssan'  

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


