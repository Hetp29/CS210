--1. Artists: Uniquely identified by name, can have albums and singles 
--2. Songs: Have title, artist, possibly album, release date, and genres 
--3. Albums: Collection of songs by an artist with a release date 
--4. Users: Uniquely identified by username, can have playlists and give ratings 
--5. Playlists: Created by users, contain songs, have title and creation date/time
--6. Ratings: User rate albums, songs, or playlists on a scale of 1-5

--artists table
CREATE TABLE artists (
    artist_id INT AUTO_INCREMENT PRIMARY KEY,
    artist_name VARCHAR(100) NOT NULL UNIQUE
);

--genres table (predefined genres)
CREATE TABLE genres (
    genre_id INT AUTO_INCREMENT PRIMARY KEY,
    genre_name VARCHAR(50) NOT NULL UNIQUE
)

--albums table
CREATE TABLE albums (
    album_id INT AUTO_INCREMENT PRIMARY KEY,
    album_name VARCHAR(200) NOT NULL,
    artist_id INT NOT NULL,
    release_date DATE NOT NULL,
    FOREIGN KEY (artist_id) REFERENCES artists(artist_id),
    UNIQUE (album_name, artist_id)
);

--songs table
CREATE TABLE songs (
    song_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    artist_id INT NOT NULL,
    album_id INT NULL,  --NULL for singles
    release_date DATE NOT NULL,
    FOREIGN KEY (artist_id) REFERENCES artists(artist_id),
    FOREIGN KEY (album_id) REFERENCES albums(album_id),
    UNIQUE (title, artist_id)
);

--songs_genres junction table
CREATE TABLE song_genres (
    song_id INT NOT NULL,
    genre_id INT NOT NULL,
    PRIMARY KEY (song_id, genre_id),
    FOREIGN KEY (song_id) REFERENCES songs(song_id),
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
);

--users table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE 
)

--playlists table
CREATE TABLE playlists (
    playlist_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    user_id INT NOT NULL,
    created_datetime DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    UNIQUE (user_id, title)
);

--playlist_songs junction table
CREATE TABLE playlist_songs (
    playlist_id INT NOT NULL,
    song_id INT NOT NULL,
    PRIMARY KEY (playlist_id, song_id),
    FOREIGN KEY (playlist_id) REFERENCES playlists(playlist_id),
    FOREIGN KEY (song_id) REFERENCES songs(song_id)
);

--ratings table
CREATE TABLE ratings (
    rating_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    rating_value INT NOT NULL CHECK (rating_value BETWEEN 1 AND 5),
    rating_date DATE NOT NULL,

    --columns identify what is being rated 
    song_id INT NULL,
    album_id INT NULL,
    playlist_id INT NULL,

    --ensure only one of song_id, album_id, or playlist_id is provided 
    CHECK ((song_id IS NOT NULL AND album_id IS NULL AND playlist_id IS NULL) OR
        (song_id IS NULL AND album_id IS NOT NULL AND playlist_id IS NULL) OR
        (song_id IS NULL AND album_id IS NULL AND playlist_id IS NOT NULL)),
    
    --ensure user cannot rate the same item multiple times on the same day 
    UNIQUE (user_id, song_id, rating_date),
    UNIQUE (user_id, album_id, rating_date),
    UNIQUE (user_id, playlist_id, rating_date)
);