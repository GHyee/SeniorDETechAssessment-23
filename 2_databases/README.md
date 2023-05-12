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

## Connecting to the PostgreSQl database
We can connect to the database using a PostgreSQL client, such as psql or pgAdmin, and start populating it with data.