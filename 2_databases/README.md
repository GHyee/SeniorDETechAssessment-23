# Databases

## Problem statement 1:
Design and implement a pipeline on cloud that processes membership applications and determine if an application is successful or unsuccessful. Applications are dropped into a location for processing.
## Cloud data pipeline Design
The data pipeline designed in [section 1](../1_data_pipelines/) is already dockerised so it can be deployed in any environment.
The data pipeline is currently reading and writing data from the mounted volume. When migrating to cloud, we can modify it to read and write from s3 instead.

### Set up Airflow and Docker on Cloud
Using AWS as an example, we can set up an Amazon Elastic Compute Cloud (EC2) instance to host the Airflow Docker container and a s3 bucket to store the files. This can be done by following the steps:
  a. Setup a EC2 instance and a s3 bucket
  b. Install Docker and Airflow on the EC2 instance.
  c. Replace the `services.webserver.build.args['S3_BUCKET_NAME']` value, `my-bucket`, to the s3 bucket name created in step a in the `docker-compose.yml` file.
  d. Copy the files in the directory, [cloud_data_pipeline](/2_databases/cloud_data_pipeline/), to a partition to the a s3 bucket.
  e. Start the Airflow Docker container using `docker-compose up --build`.
  f. Access the Airflow web UI using the public IP address of the EC2 instance and the port number specified in the `docker-compose.yml` file.
  g. Activate the data pipeline from the UI.
  h. To enable remote access to the Airflow web UI, create an inbound rule in the EC2 instance's security group that allows incoming traffic to the Airflow port (e.g. port 8080) from your IP address or a range of IP addresses.
  

Note: 
1. To deploy Airflow with high availability, consider setting up a cluster of EC2 instances and using a load balancer to distribute traffic between the instances.
2. We will need to supply AWS credentials to write to and read from an S3 bucket. One way to supply the credentials is by setting environment variables AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY which is done in [entrypoint.sh](/2_databases/cloud_data_pipeline/dockerfiles/entrypoint.sh) file during the build.


Alternatively, to run a managed service, we can also migrate the data pipeline to [Amazon Managed Workflows for Apache Airflow](https://docs.aws.amazon.com/mwaa/latest/userguide/what-is-mwaa.html).

## Problem statement 2:
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
The Airflow instance should be deployed and running on the [localhost](http://0.0.0.0:8080/admin/).

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

The below 2 SQL scripts are provided to answer the questions in the task.

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