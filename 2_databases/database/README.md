# Databases

## Problem statement:
Design a PostgreSQL database using Docker to store sales transactions and show the entity-relationship diagram.
Create tables with DDL statements to enable data consumer to perform queries.
Provide SQL statements to make query the following including:
1. Which are the top 10 members by spending
2. Which are the top 3 items that are frequently brought by members

## Database Design
The database will consist of the below two tables. The `id` column in each table is set up as a SERIAL column, which auto-increments on each new row insertion.

1. items
This table contains the below information about the items on sale:
- id: unique identifier of the item. Used as the Primary key.
- name: name of the item. Limited to 255 characters.
- manufacturer: name of the manufacturer. Limited to 255 characters.
- cost: cost of the item
- weight: weight of the item, in Kg.

2. transactions
This table contains the sales transaction. Each record represents the sales transaction carried out by a user. A transaction can contain more than one items.
- id: unique identifier of the transaction. Used as the Primary key.
- membership_id: id of the member making the transaction.
- item_ids: list of all the items sold in one transaction.
- total_price: cost of all the items sold in one transaction.
- total_weight: total weight of all the items sold in one transaction, in Kg.

### Entity-relationship diagram
+----------+         +--------------+
|   items  |         | transactions |
+----------+         +--------------+
| id       | <-----* | id           |
| name     |         | membership_id|
| manufacturer|      | item_ids     |
| cost     |         | total_price  |
| weight   |         | total_weight |
+----------+         +--------------+

The `items` table has a one-to-many relationship with the `transactions` table. Each item can appear in multiple transactions, but each transaction can only contain items from the items table. The transactions table also has a many-to-one relationship with the items table. Each transaction can contain multiple items, but each item can only appear in one transaction.


## Installation
Docker is required to run this database.
Follow the [guide](https://docs.docker.com/engine/install/) on Docker's website to install Docker engine and [docker-compose](https://docs.docker.com/compose/install/).

## Usage
To build the docker image, execute the following code:
```bash
docker build -t ecommerce-db .
```

Run the Docker container with the following command:
```bash
docker run -p 5432:5432 -d --name ecommerce-db-container ecommerce-db
```
Verify that the container is running by executing the code:
```bash
docker container ls
```

Sample output:
```
CONTAINER ID   IMAGE                         COMMAND                  CREATED          STATUS          PORTS                                       NAMES
5b760c5b81a0   ecommerce-db                  "docker-entrypoint.s…"   57 seconds ago   Up 56 seconds   0.0.0.0:5432->5432/tcp, :::5432->5432/tcp   ecommerce-db-container
```

## Interacting with the database
We can connect to the database using the `psycopg2` python package.
The database information such as name, user and password should be stored in a `.env` file. If it do not exists, run the script `generate_env_file.py` to generate it.
To run the python scripts, follow the below steps:
1. Install dependencies by running the below code.
```bash
pip install -r requirements.txt
```

2. Change to the [src](./src/) directory and execute the python script.
```bash
cd src
python -m list_tables
```
Expected output:
```
('items',)
('transactions',)
```

3. Lists of python scripts available
- list_tables: list all the tables in the database
```
python -m list_tables
```
- inject_mock_data: inject mock data into the database. 
```
python -m inject_mock_data -i 10 -t 20 -m 10
```
The arguments represents:
  - `-i`: number of items,
  - `-t`: number of transactions,
  -`-m`: number of members

- make_query: execute SQL query based on a SQL script specified
```
python -m make_query --f top_3_items.sql
```

The below 2 SQL scripts are provided in [sql_queries](./sql_queries/) folder to answer the questions in the task.

1. Which are the top 10 members by spending?
```sql
SELECT membership_id, SUM(total_price) AS total_spending
FROM transactions
GROUP BY membership_id
ORDER BY total_spending DESC
LIMIT 10;
```
This script will group the transactions by membership_id, sum up the total_price for each member, order the results by total spending in descending order, and limit the results to the top 10 members by spending.

2. Which are the top 3 items that are frequently brought by members?
```sql
SELECT items.id, items.name, COUNT(*) AS total_purchases
FROM items
JOIN transactions
ON items.id = ANY (transactions.item_ids)
GROUP BY items.id, items.name
ORDER BY total_purchases DESC
LIMIT 3;
```
This script will join the items table with the transactions table on the condition that the items.id matches any element in the transactions.item_ids array. It then groups the results by items.id and items.name, counts the number of purchases for each item, orders the results by total purchases in descending order, and limits the results to the top 3 items that are frequently bought by members.