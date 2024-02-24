import psycopg2

def connect_to_database():
    try:
        # Connect to your PostgreSQL database
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
        ("users", "id SERIAL PRIMARY KEY, email VARCHAR(100) NOT NULL, password VARCHAR(100) NOT NULL"),
        # Add more tables here as needed
    ]

    # Create tables
    for table_name, table_schema in tables:
        create_table(table_name, table_schema)


