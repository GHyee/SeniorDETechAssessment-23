import argparse
import os
import psycopg2
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--file', '-f', help='path to SQL file')
args = parser.parse_args()

# Database connection settings
DB_HOST = 'localhost'
DB_PORT = 5432
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

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

# Read SQL query from file
with open(args.file, 'r') as f:
    sql_query = f.read()

# Execute SQL query
cur.execute(sql_query)

# Get results (if any) and print them
results = cur.fetchall()
if results:
    for row in results:
        print(row)

# Commit changes and close database connection
conn.commit()
cur.close()
conn.close()
