import argparse
import os
import psycopg2
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument(
  '--num_items',
  type=int,
  default=100,
  help='number of items to generate'
)
parser.add_argument(
  '--num_transactions',
  type=int,
  default=50,
  help='number of transactions to generate'
)
args = parser.parse_args()

# Connect to database
conn = psycopg2.connect(
  database=os.getenv('DB_NAME'),
  user=os.getenv('DB_USER'),
  password=os.getenv('DB_PASSWORD'),
  host="localhost",
  port="5432"
)
cur = conn.cursor()


# Generate mock data for items table
items = []
for i in range(args.num_items):
    name = f'Item {i+1}'
    manufacturer = f'Manufacturer {random.randint(1, 10)}'
    cost = round(random.uniform(10, 1000), 2)
    weight = round(random.uniform(0.1, 50), 2)
    items.append((name, manufacturer, cost, weight))


# Insert mock data into items table
cur.executemany(
    "INSERT INTO items (name, manufacturer, cost, weight) VALUES (%s, %s, %s, %s)",
    items
)
conn.commit()


# Generate mock data for transactions table
transactions = []
for i in range(args.num_transactions):
    membership_id = random.randint(1, 10)
    item_ids = random.sample(range(1, args.num_items + 1), random.randint(1, 5))
    total_price = sum([items[id - 1][2] for id in item_ids])
    total_weight = sum([items[id - 1][3] for id in item_ids])
    transactions.append((membership_id, item_ids, total_price, total_weight))


# Insert mock data into transactions table
cur.executemany(
    "INSERT INTO transactions (membership_id, item_ids, total_price, total_weight) VALUES (%s, %s, %s, %s)",
    transactions
)
conn.commit()


# Close database connection
cur.close()
conn.close()


# Generate .env file if it doesn't exist
if not os.path.exists('.env'):
    db_user = input('Enter database user: ')
    db_password = input('Enter database password: ')
    with open('.env', 'w') as f:
        f.write(f'DB_USER={db_user}\n')
        f.write(f'DB_PASSWORD={db_password}\n')
