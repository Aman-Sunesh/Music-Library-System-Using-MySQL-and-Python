import mysql.connector as sql
from mysql.connector import Error
import hashlib
import os

def hash_password(password, salt=None):
    if salt is None:
        # Generate a new salt
        salt = os.urandom(16)

    # Use hashlib.pbkdf2_hmac for better security
    hashed = hashlib.pbkdf2_hmac('sha256', str(password).encode(), salt, 100000)

    # Return the salt and hashed password
    return salt.hex() + hashed.hex()


def authenticate_user(connection, username, password):
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT password FROM log_id WHERE name = %s", (username,))
        result = cursor.fetchone()

        if result:
            stored_password = result[0]

            # Extract salt from the stored password
            salt = bytes.fromhex(stored_password[:32])  # Assuming first 16 bytes are salt
            hashed_password = hash_password(password, salt)

            if stored_password == hashed_password:
                return True
            else:
                return False
        else:
            return False
    
    except Error as err:
        print(f"Error: {err}")
        return False
    
    finally:
        cursor.close()


def register_user(connection, username, password):
    cursor = connection.cursor()

    try:
        hashed_password = hash_password(password)
        cursor.execute("INSERT INTO log_id (name, password) VALUES (%s, %s)", (username, hashed_password))
        connection.commit()
        print(f"User '{username}' registered successfully.")
        return True
    
    except sql.Error as err:
        if err.errno == 1062:
            print(f"Username '{username}' already exists.")

        else:
            print(f"Error: {err}")

        return False
    
    finally:
        cursor.close()


