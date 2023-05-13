import os
import psycopg2
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Database connection settings
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Connect to the database
conn = psycopg2.connect(
  host=DB_HOST,
  port=DB_PORT,
  dbname=DB_NAME,
  user=DB_USER,
  password=DB_PASSWORD
)

# Create cursor
cur = conn.cursor()

# Execute a query to list all tables
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE'")

# Fetch the results
results = cur.fetchall()

# Print the results
for row in results:
    print(row)

# Close the cursor and connection
cur.close()
conn.close()
