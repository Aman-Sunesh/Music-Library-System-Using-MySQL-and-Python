import os
import mysql.connector as sql
from mysql.connector import Error

def create_connection():
    connection = None

    try:
        connection = sql.connect(host = "localhost", 
                                 user = "root", 
                                 password = "root", # Replace with your password
                                 database = "MusicLibraryDB") 
        
        if connection.is_connected():
            print("Connection to MySQL DB is successful")
        
    except Error as e:
        print(f"The error '{e}' occurred")
    
    return connection


