import os
import psycopg2
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Connect to database
conn = psycopg2.connect(
  database=os.getenv('DB_NAME'),
  user=os.getenv('DB_USER'),
  password=os.getenv('DB_PASSWORD'),
  host="localhost",
  port="5432"
)
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
