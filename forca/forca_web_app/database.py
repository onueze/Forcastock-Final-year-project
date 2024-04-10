import psycopg2

def connect_to_database():
    try:
        # Connect to PostgreSQL database
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="Alexel01",
            host="localhost",
            port="5432"
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


