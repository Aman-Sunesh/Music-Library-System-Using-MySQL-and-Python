import mysql.connector as sql
from mysql.connector import Error

def add_artist(connection, name):
    if not name.strip():
        print("Artist name cannot be empty.")
        return
    
    cursor = connection.cursor()

    try: 
        cursor.execute("INSERT INTO ARTISTS (name) VALUES (%s)", (name,))
        connection.commit()
        print(f"Artist '{name}' added successfully.")

    except sql.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()

def add_album(connection, title, artist_name, year):
    if not title.strip():
        print("Album title cannot be empty.")
        return

    cursor = connection.cursor()

    try:
        # Get artist_id from Artists table
        cursor.execute("SELECT artist_id from Artists WHERE name = %s", (artist_name,))
        result = cursor.fetchone()

        if result:
            artist_id = result[0]
        else:
            # If artist doesn't exist, add the artist
            add_artist(connection, artist_name)
            cursor.execute("SELECT artist_id FROM Artists WHERE name = %s", (artist_name,))
            artist_id = cursor.fetchone()[0]

        # Insert into Albums
        cursor.execute("INSERT INTO Albums (title, artist_id, year) VALUES (%s, %s, %s)", 
                       (title, artist_id, year))
        connection.commit()
        print(f"Album '{title}' by '{artist_name}' added successfully.")
        
    except sql.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()


def add_genre(connection, name):
    if not name.strip():
        print("Genre name cannot be empty.")
        return
    
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO Genres (name) VALUES (%s)", (name,))
        connection.commit()
        print(f"Genre '{name}' added successfully.")

    except sql.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()


def add_song(connection, title, artist_name, album_title, genre_name, duration, file_path=None):
    if not title.strip():
        print("Song title cannot be empty.")
        return
    
    cursor = connection.cursor()

    try:
        # Get or add artist
        cursor.execute("SELECT artist_id FROM Artists WHERE name = %s", (artist_name,))

        result = cursor.fetchone()

        if result:
            artist_id = result[0]

        else:
            add_artist(connection, artist_name)
            cursor.execute("SELECT artist_id FROM Artists WHERE name = %s", (artist_name,))
            artist_id = cursor.fetchone()[0]
        
        # Get or add album if album_title is provided
        if album_title:
            cursor.execute("SELECT album_id FROM Albums WHERE title = %s AND artist_id = %s", (album_title, artist_id))
            result = cursor.fetchone()

            if result:
                album_id = result[0]
            else:
                add_album(connection, album_title, artist_name, year=0)  # Replace year as necessary
                cursor.execute("SELECT album_id FROM Albums WHERE title = %s AND artist_id = %s", (album_title, artist_id))
                result = cursor.fetchone()
                album_id = result[0] if result else None
        else:
            album_id = None  # Allow album_id to be NULL
        
        # Get or add genre
        cursor.execute("SELECT genre_id FROM Genres WHERE name = %s", (genre_name,))
        result = cursor.fetchone()

        if result:
            genre_id = result[0]

        else:
            add_genre(connection, genre_name)
            cursor.execute("SELECT genre_id FROM Genres WHERE name = %s", (genre_name,))
            genre_id = cursor.fetchone()[0]
        
        # Insert into Songs
        cursor.execute("""
            INSERT INTO Songs (title, artist_id, album_id, genre_id, duration, file_path)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (title, artist_id, album_id, genre_id, duration, file_path))

        connection.commit()
        print(f"Song '{title}' added successfully.")

    except sql.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()


def view_all_songs(connection):
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT 
                Songs.song_id, 
                Songs.title, 
                Artists.name AS artist, 
                Albums.title AS album, 
                Genres.name AS genre, 
                Songs.duration, 
                Songs.file_path
            FROM 
                Songs
            LEFT JOIN 
                Artists ON Songs.artist_id = Artists.artist_id
            LEFT JOIN 
                Albums ON Songs.album_id = Albums.album_id
            LEFT JOIN 
                Genres ON Songs.genre_id = Genres.genre_id
            ORDER BY 
                Songs.song_id;
        """)

        # Fetch all the resulting rows
        rows = cursor.fetchall()
        print("\nAll Songs in Library:")

        print("-" * 80)
        print(f"{'ID':<5}{'Title':<30}{'Artist':<20}{'Album':<20}{'Genre':<15}{'Duration':<10}{'File Path'}")
        print("-" * 80)

        for row in rows:
            song_id, title, artist, album, genre, duration, file_path = row

            # Handle None values 
            duration_str = str(duration) if duration else "N/A"
            album_str = album if album else "N/A"
            artist_str = artist if artist else "N/A"
            genre_str = genre if genre else "N/A"
            file_path_str = file_path if file_path else "N/A"

            print(f"{song_id:<5}{title:<30}{artist_str:<20}{album_str:<20}{genre_str:<15}{duration_str:<10}{file_path_str}")

        print("-" * 80)


    except sql.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()


def view_all_artists(connection):
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT artist_id, name FROM Artists ORDER BY artist_id ASC")
        rows = cursor.fetchall()

        print("\nAll Artists:")
        print("-" * 40)
        print(f"{'ID':<5}{'Name'}")
        print("-" * 40)

        for row in rows:
            artist_id, name = row
            print(f"{artist_id:<5}{name}")

        print("-" * 40)

    except sql.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()


def view_all_albums(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT Albums.album_id, Albums.title, Artists.name, Albums.year
            FROM Albums
            LEFT JOIN Artists ON Albums.artist_id = Artists.artist_id
        """)
        rows = cursor.fetchall()
        print("\nAll Albums:")
        print("-" * 60)
        print(f"{'ID':<5}{'Title':<30}{'Artist':<20}{'Year'}")
        print("-" * 60)
        for row in rows:
            album_id, title, artist, year = row
            print(f"{album_id:<5}{title:<30}{artist:<20}{year}")
        print("-" * 60)
    except sql.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

def view_all_genres(connection):
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT genre_id, name FROM Genres ORDER BY genre_id")

        rows = cursor.fetchall()

        print("\nAll Genres:")

        print("-" * 40)
        print(f"{'ID':<5}{'Name'}")
        print("-" * 40)

        for row in rows:
            genre_id, name = row
            print(f"{genre_id:<5}{name}")
        print("-" * 40)

    except Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()


def search_songs_by_title(connection, title):
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT Songs.song_id, Songs.title, Artists.name, Albums.title, Genres.name, Songs.duration, Songs.file_path
            FROM Songs
            LEFT JOIN Artists ON Songs.artist_id = Artists.artist_id
            LEFT JOIN Albums ON Songs.album_id = Albums.album_id
            LEFT JOIN Genres ON Songs.genre_id = Genres.genre_id
            WHERE Songs.title LIKE %s
        """, (f"%{title}%",))
        rows = cursor.fetchall()

        print(f"\nSearch Results for Songs with Title containing '{title}':")

        print("-" * 140)
        print(f"{'ID':<5}{'Title':<30}{'Artist':<20}{'Album':<20}{'Genre':<15}{'Duration':<10}{'File Path'}")
        print("-" * 140)

        for row in rows:
            song_id, title, artist, album, genre, duration, file_path = row
            print(f"{song_id:<5}{title:<30}{artist:<20}{album:<20}{genre:<15}{str(duration):<10}{file_path}")

        print("-" * 140)

    except sql.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()


def search_songs_by_artist(connection, artist_name):
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT Songs.song_id, Songs.title, Artists.name, Albums.title, Genres.name, Songs.duration, Songs.file_path
            FROM Songs
            LEFT JOIN Artists ON Songs.artist_id = Artists.artist_id
            LEFT JOIN Albums ON Songs.album_id = Albums.album_id
            LEFT JOIN Genres ON Songs.genre_id = Genres.genre_id
            WHERE Artists.name LIKE %s
        """, (f"%{artist_name}%",))
        rows = cursor.fetchall()

        print(f"\nSearch Results for Songs by Artist '{artist_name}':")

        print("-" * 140)
        print(f"{'ID':<5}{'Title':<30}{'Artist':<20}{'Album':<20}{'Genre':<15}{'Duration':<10}{'File Path'}")
        print("-" * 140)

        for row in rows:
            song_id, title, artist, album, genre, duration, file_path = row
            print(f"{song_id:<5}{title:<30}{artist:<20}{album:<20}{genre:<15}{str(duration):<10}{file_path}")

        print("-" * 140)

    except sql.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()


def search_songs_by_album(connection, album_title):
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT Songs.song_id, Songs.title, Artists.name, Albums.title, Genres.name, Songs.duration, Songs.file_path
            FROM Songs
            LEFT JOIN Artists ON Songs.artist_id = Artists.artist_id
            LEFT JOIN Albums ON Songs.album_id = Albums.album_id
            LEFT JOIN Genres ON Songs.genre_id = Genres.genre_id
            WHERE Albums.title LIKE %s
        """, (f"%{album_title}%",))
        rows = cursor.fetchall()

        print(f"\nSearch Results for Songs in Album '{album_title}':")

        print("-" * 140)
        print(f"{'ID':<5}{'Title':<30}{'Artist':<20}{'Album':<20}{'Genre':<15}{'Duration':<10}{'File Path'}")
        print("-" * 140)

        for row in rows:
            song_id, title, artist, album, genre, duration, file_path = row
            print(f"{song_id:<5}{title:<30}{artist:<20}{album:<20}{genre:<15}{str(duration):<10}{file_path}")

        print("-" * 140)

    except sql.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()


def search_songs_by_genre(connection, genre_name):
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT Songs.song_id, Songs.title, Artists.name, Albums.title, Genres.name, Songs.duration, Songs.file_path
            FROM Songs
            LEFT JOIN Artists ON Songs.artist_id = Artists.artist_id
            LEFT JOIN Albums ON Songs.album_id = Albums.album_id
            LEFT JOIN Genres ON Songs.genre_id = Genres.genre_id
            WHERE Genres.name LIKE %s
        """, (f"%{genre_name}%",))
        rows = cursor.fetchall()

        print(f"\nSearch Results for Songs in Genre '{genre_name}':")

        print("-" * 80)
        print(f"{'ID':<5}{'Title':<30}{'Artist':<20}{'Album':<20}{'Genre':<15}{'Duration':<10}{'File Path'}")
        print("-" * 80)

        for row in rows:
            song_id, title, artist, album, genre, duration, file_path = row
            
            # Handle None values gracefully
            duration_str = str(duration) if duration else "N/A"
            album_str = album if album else "N/A"
            artist_str = artist if artist else "N/A"
            genre_str = genre if genre else "N/A"
            file_path_str = file_path if file_path else "N/A"

            print(f"{song_id:<5}{title:<30}{artist_str:<20}{album_str:<20}{genre_str:<15}{duration_str:<10}{file_path_str}")

        print("-" * 80)

    except sql.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()


def search_songs_by_year(connection, year):
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT Songs.song_id, Songs.title, Artists.name, Albums.title, Genres.name, Songs.duration, Songs.file_path
            FROM Songs
            LEFT JOIN Artists ON Songs.artist_id = Artists.artist_id
            LEFT JOIN Albums ON Songs.album_id = Albums.album_id
            LEFT JOIN Genres ON Songs.genre_id = Genres.genre_id
            WHERE Albums.year = %s
        """, (year,))
        rows = cursor.fetchall()

        print(f"\nSearch Results for Songs Released in Year '{year}':")

        print("-" * 80)
        print(f"{'ID':<5}{'Title':<30}{'Artist':<20}{'Album':<20}{'Genre':<15}{'Duration':<10}{'File Path'}")
        print("-" * 80)

        for row in rows:
            song_id, title, artist, album, genre, duration, file_path = row
            print(f"{song_id:<5}{title:<30}{artist:<20}{album:<20}{genre:<15}{str(duration):<10}{file_path}")

        print("-" * 80)

    except sql.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()


def update_song(connection, song_id, field, new_value):
    cursor = connection.cursor()
    try:
        # Map user-friendly field names to database column names
        field_mapping = {
            'title': 'title',
            'artist': 'artist_id',
            'album': 'album_id',
            'genre': 'genre_id',
            'duration': 'duration',
            'file_path': 'file_path'
        }

        if field not in field_mapping:
            print("Invalid field name.")
            return

        if field == 'artist':
            # Get or add artist
            cursor.execute("SELECT artist_id FROM Artists WHERE name = %s", (new_value,))
            result = cursor.fetchone()
            if result:
                new_value = result[0]
            else:
                add_artist(connection, new_value)
                cursor.execute("SELECT artist_id FROM Artists WHERE name = %s", (new_value,))
                new_value = cursor.fetchone()[0]

        elif field == 'album':
            # Get or add album (Assuming artist is known or fetched)
            cursor.execute("SELECT album_id FROM Albums WHERE title = %s", (new_value,))
            result = cursor.fetchone()
            if result:
                new_value = result[0]
            else:
                # For simplicity, add album with no associated artist and year
                add_album(connection, new_value, artist_name="Unknown", year=0)
                cursor.execute("SELECT album_id FROM Albums WHERE title = %s", (new_value,))
                new_value = cursor.fetchone()[0]

        elif field == 'genre':
            # Get or add genre
            cursor.execute("SELECT genre_id FROM Genres WHERE name = %s", (new_value,))
            result = cursor.fetchone()
            if result:
                new_value = result[0]
            else:
                add_genre(connection, new_value)
                cursor.execute("SELECT genre_id FROM Genres WHERE name = %s", (new_value,))
                new_value = cursor.fetchone()[0]

        # Update the field
        cursor.execute(f"UPDATE Songs SET {field_mapping[field]} = %s WHERE song_id = %s", (new_value, song_id))
        connection.commit()
        print(f"Song ID {song_id} updated successfully.")
    except sql.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()


def delete_song(connection, song_id):
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM Songs WHERE song_id = %s", (song_id, ))
        connection.commit()

        if cursor.rowcount:
            print(f"Song ID {song_id} deleted successfully.")
        else:
            print(f"No song found with ID {song_id}.")


    except sql.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()

        
def view_statistics(connection):
    cursor = connection.cursor(dictionary=True)

    try:
        print("\n--- Music Library Statistics ---")
        
        # 1. Total Number of Songs
        cursor.execute("SELECT COUNT(*) AS total_songs FROM Songs")
        total_songs = cursor.fetchone()['total_songs']
        print(f"Total Number of Songs: {total_songs}")
        
        # 2. Number of Songs by Genre
        cursor.execute("""
            SELECT Genres.name AS genre, COUNT(Songs.song_id) AS count
            FROM Songs
            LEFT JOIN Genres ON Songs.genre_id = Genres.genre_id
            GROUP BY Genres.name
            ORDER BY count DESC
        """)
        genres = cursor.fetchall()
        print("\nNumber of Songs by Genre:")
        print("-" * 30)

        for genre in genres:
            genre_name = genre['genre'] if genre['genre'] else 'Unknown'
            print(f"{genre_name}: {genre['count']}")
        
        # 3. Top Artists (Most Songs)
        cursor.execute("""
            SELECT Artists.name AS artist, COUNT(Songs.song_id) AS count
            FROM Songs
            LEFT JOIN Artists ON Songs.artist_id = Artists.artist_id
            GROUP BY Artists.name
            ORDER BY count DESC
            LIMIT 5
        """)

        top_artists = cursor.fetchall()

        print("\nTop 5 Artists (Most Songs):")

        print("-" * 30)
        for artist in top_artists:
            artist_name = artist['artist'] if artist['artist'] else 'Unknown'
            print(f"{artist_name}: {artist['count']} songs")
        
        # 4. Albums Overview (Number of Albums and Songs per Album)
        cursor.execute("""
            SELECT Albums.title AS album, Artists.name AS artist, COUNT(Songs.song_id) AS song_count
            FROM Albums
            LEFT JOIN Artists ON Albums.artist_id = Artists.artist_id
            LEFT JOIN Songs ON Songs.album_id = Albums.album_id
            GROUP BY Albums.album_id
            ORDER BY song_count DESC
        """)
        albums = cursor.fetchall()

        print("\nAlbums Overview:")
        print("-" * 50)
        for album in albums:
            album_title = album['album'] if album['album'] else 'Unknown'
            artist_name = album['artist'] if album['artist'] else 'Unknown'
            song_count = album['song_count']
            print(f"Album: {album_title} | Artist: {artist_name} | Songs: {song_count}")
    
    except Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()