import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()



def connect_to_database():
    # Get database connection parameters from environment variables
    db_name = os.environ.get('DB_NAME')
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    db_host = os.environ.get('DB_HOST')
    db_port = int(os.environ.get('DB_PORT'))
    
    try:
        # Connect to PostgreSQL database
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
            sslmode='require'
        )
        print("Connected to the database")
        return conn
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return None
    

def create_table(table_name, table_schema):
    conn = connect_to_database()
    cur = conn.cursor()

    try:
        # SQL command to create the table
        sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {table_schema}
        );
        """

        # Execute the SQL command
        cur.execute(sql)

        # Commit the transaction
        conn.commit()

        print(f"Table {table_name} created successfully!")

    except Exception as e:
        print(f"Error creating table {table_name}: {e}")

    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()

def create_all_tables():
    # Define table names and schemas
    tables = [
        ("users", "id SERIAL PRIMARY KEY, email VARCHAR(100) NOT NULL"),
        ("demo_accounts", "demo_id SERIAL PRIMARY KEY, allocated_amount DECIMAL(10, 2) NOT NULL, user_id INT NOT NULL, FOREIGN KEY (user_id) REFERENCES users(id)"),
        ("transactions", "transaction_id SERIAL PRIMARY KEY, transaction_type VARCHAR(5) NOT NULL CHECK (transaction_type IN ('BUY', 'SELL')), stock_symbol VARCHAR(10) NOT NULL, quantity INT NOT NULL, price DECIMAL(10, 2) NOT NULL, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, demo_id INT NOT NULL, status VARCHAR(10) NOT NULL DEFAULT 'OPEN' CHECK (status IN ('OPEN', 'CLOSED')), FOREIGN KEY (demo_id) REFERENCES demo_accounts(demo_id)"),
        # Add more tables here 
    ]

    # Create tables
    for table_name, table_schema in tables:
        create_table(table_name, table_schema)


