import psycopg2
from dotenv import load_dotenv
import os
import yaml
import argparse
from typing import List, Dict


# Load environment variables from .env file
load_dotenv()

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--config_path', '-c', type=str,
                    default='../config/user_config.yaml',
                    help='file path of the user config file')
args = parser.parse_args()

# Get database credentials from environment variables
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

# Create a cursor object to execute queries
cur = conn.cursor()


def create_user(username: str, password: str) -> None:
    """Creates a new database user with the specified username and password.

    Args:
        username (str): The username of the new user to create.
        password (str): The password of the new user to create.

    Raises:
        psycopg2.Error: If there was an error creating the user.
    """
    try:
        cur.execute(f"SELECT COUNT(*) FROM pg_user WHERE usename = '{username}'")
        result = cur.fetchone()
        user_exists = result[0] > 0

        if not user_exists:
            cur.execute(f"CREATE USER {username} WITH PASSWORD '{password}'")
            conn.commit()
            print(f"User '{username}' created successfully!")
    except psycopg2.Error as e:
        print(f"Error creating user '{username}': {e}")


def grant_permissions(username: str, permissions: List[Dict[str, str]]) -> None:
    """
    Grants the specified permissions to the specified database user.

    Args:
        username (str): The name of the user to grant permissions to.
        permissions (List[Dict[str, str]]): A list of dictionaries representing the permissions to grant.
            Each dictionary should have the keys 'table_name' and 'permission_type'.

    Raises:
        psycopg2.Error: If there is an error executing the SQL command.

    """
    for permission in permissions:
        table_name = permission['table_name']
        permission_type = permission['permission_type']
        try:
            cur.execute(f"GRANT {permission_type} ON {table_name} TO {username}")
            print(f"User {username} permission - {permission_type} has been successfully granted on {table_name}.")
        except psycopg2.Error as e:
            print(f"Error granting permission for user {username} on table {table_name}: {e}")
    conn.commit()


def create_user_and_grant_permissions(user_config: dict) -> None:
    """Creates a new database user and grants the specified permissions based on the provided configuration."""
    username = user_config['username']
    password = user_config['password']
    permissions = user_config['permissions']

    create_user(username, password)
    grant_permissions(username, permissions)


# Load user configuration from YAML file
with open(args.config_path, "r") as f:
    user_configs = yaml.load(f, Loader=yaml.SafeLoader)

# Create users and grant permissions based on configuration
for user_config in user_configs:
    create_user_and_grant_permissions(user_config)

# Close the cursor and database connection
cur.close()
conn.close()
