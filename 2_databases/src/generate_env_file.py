import os


# Generate .env file if it doesn't exist
if not os.path.exists('.env'):
    db_name = input('Enter database name: ')
    db_user = input('Enter database user: ')
    db_password = input('Enter database password: ')
    with open('.env', 'w') as f:
        f.write(f'DB_NAME={db_name}\n')
        f.write(f'DB_USER={db_user}\n')
        f.write(f'DB_PASSWORD={db_password}\n')
else:
    print('.env file already exists.')
