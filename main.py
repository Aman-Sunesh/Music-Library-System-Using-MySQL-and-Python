import mysql.connector as sql
from mysql.connector import Error
import time
import pygame
import os
import sys

# main.py
import sys
from db_connection import create_connection
from authentication import authenticate_user, register_user
from music_player import play_music
from crud_operations import view_statistics 
from crud_operations import (
    add_artist, add_album, add_genre, add_song,
    view_all_songs, view_all_artists, view_all_albums, view_all_genres,
    search_songs_by_title, search_songs_by_artist, search_songs_by_album,
    search_songs_by_genre, search_songs_by_year,
    update_song, delete_song
)


def print_menu():
    print("\n===============================================")
    print("              MUSIC LIBRARY SYSTEM             ")
    print("           ", time.ctime())
    print("===============================================")
    print("1. Play Music")
    print("2. Add New Artist")
    print("3. Add New Album")
    print("4. Add New Genre")
    print("5. Add New Song")
    print("6. View All Songs")
    print("7. View All Artists")
    print("8. View All Albums")
    print("9. View All Genres")
    print("10. Search Songs by Title")
    print("11. Search Songs by Artist")
    print("12. Search Songs by Album")
    print("13. Search Songs by Genre")
    print("14. Search Songs by Year")
    print("15. Update Song Details")
    print("16. Delete a Song")
    print("17. Register New User")  
    print("18. View your Music Statistics")
    print("19. Exit")
    print("===============================")

def main():
    connection = create_connection()
    if not connection:
        sys.exit()

    print()
    print()
    print("Welcome to the Music Library System!")
    print("Please log in to continue.")

    authenticated = False

    while not authenticated:
        while True:
            print()
            print("1. Register new user")
            print("2. Login")
            print("3. Exit")
            print()

            try:
                ch = int(input("Enter your choice(1-3): "))
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 3.")
                continue

            if ch==1:
                    # User Registration
                    print("\n--- Register New User ---")

                    new_username = input("Enter new username: ")
                    new_password_input = input("Enter new password (integer): ")

                    if not new_password_input.isdigit():
                        print("Password must be an integer.")
                        continue

                    new_password = int(new_password_input)
                    register_user(connection, new_username, new_password)

                    print("Please login to continue")
                    time.sleep(3)  # Delays for 3 seconds
                    continue
                
            elif ch==2:
                while not authenticated:
                    username = input("Username: ")
                    password_input = input("Password (integer): ")

                    if not password_input.isdigit():
                        print("Password must be an integer.")
                        continue

                    password = int(password_input)
                    
                    if authenticate_user(connection, username, password):
                        print(f"Login successful. Welcome, {username}!")
                        authenticated = True
                        break

                    else:
                        print("Invalid username or password. Please try again.")

                if authenticated:
                    break  

            elif ch==3:
                sys.exit()
            
            else:
                print("Invalid choice. Please enter a number between 1 and 3.")


    while True:
        print_menu()

        choice = input("Enter your choice (1-19): ")

        if choice == '1':
            play_music(connection)
        

        elif choice == '2':
            name = input("Enter artist name: ")
            add_artist(connection, name)

        elif choice == '3':
            title = input("Enter album title: ")
            artist = input("Enter artist name: ")
            year = input("Enter release year: ")

            if not year.isdigit():
                print("Year must be a number.")
                continue

            add_album(connection, title, artist, int(year))

        elif choice == '4':
            name = input("Enter genre name: ")
            add_genre(connection, name)

        elif choice == '5':
            title = input("Enter song title: ").strip()
            if not title:
                print("Song title cannot be empty.")
                continue

            artist = input("Enter artist name: ").strip()
            if not artist:
                print("Artist name cannot be empty.")
                continue

            album = input("Enter album title: ").strip()


            genre = input("Enter genre: ").strip()
            if not genre:
                print("Genre cannot be empty.")
                continue

            duration = input("Enter duration (HH:MM:SS or MM:SS): ").strip()
            if not duration:
                print("Duration cannot be empty.")
                continue

            file_path = input("Enter file path (optional): ").strip() or None
            add_song(connection, title, artist, album, genre, duration, file_path)

        elif choice == '6':
            view_all_songs(connection)

        elif choice == '7':
            view_all_artists(connection)

        elif choice == '8':
            view_all_albums(connection)

        elif choice == '9':
            view_all_genres(connection)

        elif choice == '10':
            title = input("Enter song title to search: ")
            search_songs_by_title(connection, title)

        elif choice == '11':
            artist = input("Enter artist name to search: ")
            search_songs_by_artist(connection, artist)

        elif choice == '12':
            album = input("Enter album title to search: ")
            search_songs_by_album(connection, album)

        elif choice == '13':
            genre = input("Enter genre to search: ")
            search_songs_by_genre(connection, genre)

        elif choice == '14':
            year = input("Enter release year to search: ")
            if not year.isdigit():
                print("Year must be a number.")
                continue
            search_songs_by_year(connection, int(year))

        elif choice == '15':
            song_id = input("Enter song ID to update: ")
            if not song_id.isdigit():
                print("Song ID must be a number.")
                continue
            field = input("Enter field to update (title, artist, album, genre, duration, file_path): ").lower()
            new_value = input(f"Enter new value for {field}: ")
            update_song(connection, int(song_id), field, new_value)

        elif choice == '16':
            song_id = input("Enter song ID to delete: ")
            if not song_id.isdigit():
                print("Song ID must be a number.")
                continue
            confirm = input(f"Are you sure you want to delete song ID {song_id}? (y/n): ").lower()
            if confirm == 'y':
                delete_song(connection, int(song_id))
            else:
                print("Deletion cancelled.")

        elif choice == '17':
            # User Registration
            print("\n--- Register New User ---")

            new_username = input("Enter new username: ")
            new_password_input = input("Enter new password (integer): ")

            if not new_password_input.isdigit():
                print("Password must be an integer.")
                continue

            new_password = int(new_password_input)
            register_user(connection, new_username, new_password)

        elif choice == '18':
            view_statistics(connection)


        elif choice == '19':
            print("Exiting Music Library System. Goodbye!")
            connection.close()
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 19.")

if __name__ == "__main__":
    main()
