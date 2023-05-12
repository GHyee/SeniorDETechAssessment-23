# Design 1 - Databases User Management

## Problem statement
Design a database that will be used by several teams within the company to track the orders of members. Implement a strategy for accessing this database based on the various teams' needs.

## Database Design

### Database setup
The database is created in section 2 and it contains two tables.
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

### User Management Setup
To implement a strategy for accessing the ecommerce database based on the needs of the various teams, we can:
- create separate user accounts for each team with appropriate access permissions based on their needs.
- grant **read-only** access to the `transactions` and `items` table for the **Logistics** and **Analytics** teams. They should be able to query the tables and view the data, but not perform any updates.
- grant **read** and **write** access to the `items` table for the **Sales** team, allowing them to add new items and remove old items.
- grant **read** and **write** access to the `transactions` table for the **Logistics** team, allowing them to update the table for completed transactions.

Note: the access credentials should stored securely. One way is to store it in a `.env` file which should not be pushed to version control. However, for the sake of the assessment, the `.env` has been committed to this repository.

By implementing these access permissions, we can ensure that each team has access to the data they need to perform their tasks without being able to modify data they shouldn't be able to modify.

Assuming that the ecommerce database in Section 2. Databases
Follow the below steps to set up the above mentioned user management.

1. Create a [.env](/3_system_design/design_1/src/.env) file in the `src` folder to store the secrets.

2. Creata a user configuration YAML file, [user_config.yaml](/3_system_design/design_1/config/user_config.yaml) that contains user specific information such as username, password, and permission types for each table.
```yaml
- username: userA
  password: ${USERA_PASSWORD}
  permissions:
    - table_name: transactions
      permission_type: SELECT
    - table_name: transactions
      permission_type: UPDATE
```
Note that the password should not be stored as code for security purpose. For this assessment, the password will be stored in the `.env` file created in step 1.

3. Install the required python packages.
```bash
pip install -r requirements.txt 
```

4. Check that the postgreSql database is running.
```bash
docker container ls
```
Expected output:
```
CONTAINER ID   IMAGE                         COMMAND                  CREATED        STATUS        PORTS                                       NAMES
5b760c5b81a0   ecommerce-db                  "docker-entrypoint.s…"   6 hours ago    Up 6 hours    0.0.0.0:5432->5432/tcp, :::5432->5432/tcp   ecommerce-db-container
```

5. Execute the python scripts.
```bash
cd src
python -m create_user -c ../config/user_config.yaml
```

Expected output:
```
User logistics permission - SELECT has been successfully granted on transactions.
User logistics permission - UPDATE has been successfully granted on transactions.
User analytics permission - SELECT has been successfully granted on transactions.
User analytics permission - SELECT has been successfully granted on items.
User sales permission - SELECT has been successfully granted on items.
User sales permission - INSERT has been successfully granted on items.
User sales permission - UPDATE has been successfully granted on items.
User sales permission - DELETE has been successfully granted on items.
```