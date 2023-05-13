import argparse
import os
import random
import psycopg2
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--items', '-i', type=int, default=50, help='number of items to insert')
parser.add_argument('--transactions', '-t', type=int, default=100, help='number of transactions to insert')
parser.add_argument('--members', '-m', type=int, default=10, help='number of members to insert')
args = parser.parse_args()

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

# Generate mock data
items = []
for i in range(args.items):
    item_name = f'Item {i+1}'
    item_manufacturer = f'Manufacturer {i+1}'
    item_cost = round(random.uniform(10, 1000), 2)
    item_weight = round(random.uniform(0.1, 50), 2)
    items.append((item_name, item_manufacturer, item_cost, item_weight))

transactions = []
for i in range(args.transactions):
    member_id = random.randint(1, args.members)
    item_ids = random.sample(range(1, args.items + 1), random.randint(1, 5))
    total_price = sum([items[id - 1][2] for id in item_ids])
    total_weight = sum([items[id - 1][3] for id in item_ids])
    transactions.append((member_id, item_ids, total_price, total_weight))

# Insert mock data into the database
cur.executemany('INSERT INTO items (name, manufacturer, cost, weight) VALUES (%s, %s, %s, %s)', items)
cur.executemany('INSERT INTO transactions (membership_id, item_ids, total_price, total_weight) VALUES (%s, %s, %s, %s)',
                transactions)

# Commit changes and close database connection
conn.commit()
cur.close()
conn.close()

# Print summary of added data
print(f'Added {len(items)} items to the database.')
print(f'Added {len(transactions)} transactions to the database.')
