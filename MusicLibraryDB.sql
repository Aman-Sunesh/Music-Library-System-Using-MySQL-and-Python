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
