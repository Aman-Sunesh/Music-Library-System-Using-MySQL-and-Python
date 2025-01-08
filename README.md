# Music Library System

## Overview
The **Music Library System** is a console-based application that allows users to manage their personal music collections efficiently. Built using Python, this tool provides functionalities to add, view, search, update, and delete music records, as well as organize and export/import the library. Additionally, it includes a music playback feature powered by Pygame and secure user authentication with hashed and salted passwords.

## Prerequisites
Before you can run this application, ensure you have the following installed:

- **Python 3.8 or higher**
- **MySQL Server**
- **Pygame**
- **mysql-connector-python**

## Installation

### Python Installation
Download and install Python from [python.org](https://www.python.org/downloads/).

### MySQL Server Installation
- **For macOS (using Homebrew):**
    ```bash
    brew install mysql
    ```
    
- **For Windows:**
    - Download and install [MySQL Community Server](https://dev.mysql.com/downloads/mysql/).
      
- **For Linux (Ubuntu/Debian-based systems):**
    ```bash
    sudo apt update
    sudo apt install mysql-server
    ```

### Library Installation
Use `pip` to install the required Python libraries:
```bash
pip install mysql-connector-python pygame
```

### Clone the Repository
```bash
git clone https://github.com/yourusername/Music-Library-System-Using-MySQL-and-Python.git
cd Music-Library-System-Using-MySQL-and-Python
```

## Database Setup

### Create the Database and Tables

#### Start MySQL Server:

**macOS/Linux:**

```bash
sudo service mysql start
```

**Windows: Start the MySQL service from the Services panel or use the MySQL Workbench.**

#### Create Database and Tables:

**1. Access MySQL Shell:**

To access the MySQL shell, use the following command in your terminal:

```bash
mysql -u root -p
```

**Create Database and Tables:**

```bash
-- Create the MusicLibraryDB database
CREATE DATABASE MusicLibraryDB;

-- Use the database
USE MusicLibraryDB;

-- Create Artists table
CREATE TABLE Artists (
    artist_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

-- Create Albums table
CREATE TABLE Albums (
    album_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist_id INT,
    year INT,
    FOREIGN KEY (artist_id) REFERENCES Artists(artist_id) ON DELETE SET NULL
);

-- Create Genres table
CREATE TABLE Genres (
    genre_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

-- Create Songs table
CREATE TABLE Songs (
    song_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist_id INT,
    album_id INT,
    genre_id INT,
    duration TIME,
    file_path VARCHAR(500),
    FOREIGN KEY (artist_id) REFERENCES Artists(artist_id) ON DELETE SET NULL,
    FOREIGN KEY (album_id) REFERENCES Albums(album_id) ON DELETE SET NULL,
    FOREIGN KEY (genre_id) REFERENCES Genres(genre_id) ON DELETE SET NULL
);

-- Create Users table for authentication
CREATE TABLE log_id (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(512) NOT NULL
);
```

## Configuration

### Database Credentials

Open `db_connection.py` and update the user, password, host, and database parameters with your MySQL credentials:

```python
connection = sql.connect(
    host="localhost",
    user="your_mysql_username",
    password="your_mysql_password",  # Replace with your password
    database="MusicLibraryDB"
)
```

## Usage

To run the application, navigate to the application directory and execute the following command:

```bash
python main.py
```

## User Authentication
Upon starting the application, users are prompted to either register or log in.

### Register New User
- **Username**: Enter a unique username.
- **Password**: Enter a password (integer). The password is hashed with a unique salt for security.

### Login
- **Username**: Enter your registered username.
- **Password**: Enter your password (integer). The application verifies the hashed password.

## Features and Functionalities

1. **Play Music**
   - Displays a list of available songs with their IDs and titles.
   - Select a song by entering its ID to play.
   - **Controls During Playback**:
     - **P**: Pause
     - **R**: Resume
     - **N**: Next Song
     - **B**: Previous Song
     - **Q**: Quit Playback

2. **Add New Artist**
   - Enter the name of a new artist to add to the library.

3. **Add New Album**
   - Enter album details including title, artist name, and release year.
   - Automatically adds the artist if they do not exist.

4. **Add New Genre**
   - Enter the name of a new genre to categorize songs.

5. **Add New Song**
   - Enter song details including title, artist, album, genre, duration, and optional file path.
   - Automatically handles adding new artists, albums, and genres if they do not exist.

6. **View All Songs**
   - Displays a list of all songs with detailed information.

7. **View All Artists**
   - Lists all artists in the library.

8. **View All Albums**
   - Lists all albums along with their respective artists and release years.

9. **View All Genres**
   - Lists all genres in the library.

10. **Search Songs by Title**
    - Search for songs containing a specific title keyword.

11. **Search Songs by Artist**
    - Search for songs by a specific artist.

12. **Search Songs by Album**
    - Search for songs within a specific album.

13. **Search Songs by Genre**
    - Search for songs within a specific genre.

14. **Search Songs by Year**
    - Search for songs released in a specific year.

15. **Update Song Details**
    - Update details of an existing song by entering its ID and specifying the field to update.

16. **Delete a Song**
    - Remove a song from the library by entering its ID.

17. **Register New User**
    - Register additional users with unique usernames and secure passwords.

18. **View your Music Statistics**
    - View various statistics such as total number of songs, songs by genre, top artists, and albums overview.

19. **Exit**
    - Safely exits the application, ensuring all data is saved.

## Password Security
- **Hashing with Salt**: Passwords are hashed using the SHA-256 algorithm with a unique salt for each user.
- **How It Works**:
  - **Registration**: Upon registration, a unique salt is generated using `os.urandom(16)`. The password is hashed using `hashlib.pbkdf2_hmac` with the generated salt. The salt and hashed password are concatenated and stored in the `log_id` table.
  - **Authentication**: During login, the stored salt is extracted from the stored hashed password. The entered password is hashed with the extracted salt. The newly hashed password is compared with the stored hash to verify authenticity.

## Database Operations
- **Artists, Albums, Genres, Songs**:
  - **Add Operations**: Functions to add new artists, albums, genres, and songs, handling duplicates and relationships.
  - **View Operations**: Functions to view all songs, artists, albums, and genres with detailed information.
  - **Search Operations**: Functions to search songs by title, artist, album, genre, and year.
  - **Update Operations**: Function to update song details, including handling related entities like artists and albums.
  - **Delete Operations**: Function to delete songs from the library.

## Music Playback
- **Play Music**: Lists available songs with valid file paths. Uses Pygame to handle audio playback. Provides controls to pause, resume, skip to the next song, go back to the previous song, or quit playback.

## Statistics and Reports
- **View Statistics**: Displays total number of songs, number of songs by genre, top 5 artists with the most songs, and an albums overview, including the number of songs per album.

## Important Notes
- **Password Security**: Ensures that user passwords are protected from being easily compromised.
- **Database Connection**: Ensure that the `db_connection.py` file contains the correct MySQL credentials. Avoid hardcoding sensitive information; consider using environment variables or a configuration file for enhanced security.
- **File Handling**: The tool writes the compressed data to `encoded_file.txt` in the same directory as the executable. Ensure you have write permissions for this directory.
- **Character Encoding**: The tool handles standard ASCII characters. Special characters or different encodings may require additional handling.

## Troubleshooting
- **Compilation/Execution Errors**: Ensure all required libraries are installed (`mysql-connector-python`, `pygame`) and the source code is free from syntax errors.
- **Database Connection Errors**: Verify your MySQL credentials in `db_connection.py` and ensure that the MySQL server is running.
- **File Not Found**: Ensure that `encoded_file.txt` exists in the directory and that the program has the necessary permissions to read/write files.
- **Decoded Text Mismatch**: Check the encoding and decoding logic for correctness. Ensure that the entire compression-decompression cycle is correctly implemented without data loss.
- **Runtime Errors**: Use debugging tools or add additional print statements to trace the program's execution. Ensure that all edge cases are handled, such as end-of-file conditions and empty inputs.
- **Password Issues**: Verify that passwords are entered as integers during registration and login. Ensure that the hashing and salting mechanisms are functioning correctly.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your improvements or additional features. Whether it's enhancing the algorithm, optimizing performance, or adding new functionalities, your contributions are valuable.

## Acknowledgments
- [MySQL Connector/Python Documentation](https://dev.mysql.com/doc/connector-python/en/)
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Hashlib Documentation](https://docs.python.org/3/library/hashlib.html)
- [Python Documentation](https://docs.python.org/3/)
