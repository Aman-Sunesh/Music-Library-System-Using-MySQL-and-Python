import pygame
import time
import os
from crud_operations import view_all_songs 

def play_music(connection):
    cursor = connection.cursor(dictionary=True)

    try:
        # Fetch all songs with their IDs and file paths
        cursor.execute("""
            SELECT song_id, title, file_path
            FROM Songs
            WHERE file_path IS NOT NULL AND file_path != ''
            ORDER BY song_id
        """)
        songs = cursor.fetchall()

        if not songs:
            print("No songs available to play. Please add songs with valid file paths.")
            return

        # Display the list of songs
        print("\nAvailable Songs:")
        print("-" * 50)
        print(f"{'ID':<5}{'Title'}")
        print("-" * 50)

        for index, song in enumerate(songs, start=1):
            print(f"{song['song_id']:<5}{song['title']}")

        print("-" * 50)

        # Prompt user to select a song by ID
        song_id_input = input("Enter the Song ID you want to play: ")

        if not song_id_input.isdigit():
            print("Invalid input. Song ID must be a number.")
            return

        song_id = int(song_id_input)

        # Find the selected song's index
        selected_index = None
        for index, song in enumerate(songs):
            if song['song_id'] == song_id:
                selected_index = index
                break

        if selected_index is None:
            print(f"No song found with ID {song_id}.")
            return

        # Initialize pygame mixer once
        pygame.mixer.init()

        while True:
            current_song = songs[selected_index]
            file_path = current_song['file_path']
            title = current_song['title']

            # Check if the file exists
            if not os.path.isfile(file_path):
                print(f"The file '{file_path}' does not exist.")
                # Remove the song from the list
                del songs[selected_index]
                if not songs:
                    print("No more songs available to play.")
                    return
                # Adjust index if necessary
                if selected_index >= len(songs):
                    selected_index = 0
                continue

            # Load and play the song
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            print(f"\nNow Playing: {title}")
            print("Controls: [P]ause, [R]esume, [N]ext, [B]ack, [Q]uit Playback")

            paused = False

            while True:
                # Check if the song has ended
                if not pygame.mixer.music.get_busy() and not paused:
                    print("Song has ended. Moving to the next song.")
                    selected_index += 1
                    if selected_index >= len(songs):
                        selected_index = 0  # Wrap around to the first song
                    break  # Break to load the next song

                command = input("Enter command: ").strip().lower()

                if command == 'p':
                    if not paused:
                        pygame.mixer.music.pause()
                        paused = True
                        print("Music Paused.")
                    else:
                        print("Music is already paused.")
                elif command == 'r':
                    if paused:
                        pygame.mixer.music.unpause()
                        paused = False
                        print("Music Resumed.")
                    else:
                        print("Music is not paused.")
                elif command == 'n':
                    pygame.mixer.music.stop()
                    print("Moving to the next song.")
                    selected_index += 1
                    if selected_index >= len(songs):
                        selected_index = 0  # Wrap around to the first song
                    break  # Break to load the next song
                elif command == 'b':
                    pygame.mixer.music.stop()
                    print("Moving to the previous song.")
                    selected_index -= 1
                    if selected_index < 0:
                        selected_index = len(songs) - 1  # Wrap around to the last song
                    break  # Break to load the previous song
                elif command == 'q':
                    pygame.mixer.music.stop()
                    print("Exiting Playback.")
                    pygame.mixer.quit()
                    return  # Exit the function to return to the main menu
                else:
                    print("Invalid command. Use [P], [R], [N], [B], or [Q].")

    except Exception as e:
        print(f"An error occurred during playback: {e}")

    finally:
        pygame.mixer.quit()
        cursor.close()