--for 10 required queries 

--Which 3 genres are most represented in terms of number of songs in that genre?
SELECT g.genre_name AS genre, COUNT(sg.song_id) AS number_of_songs
FROM genres g
JOIN song_genres sg ON g.genre_id = sg.genre_id
GROUP BY g.genre_id, g.genre_name
ORDER BY number_of_songs DESC
LIMIT 3;

--Find names of artists who have songs that are in albums as well as outside of albums (singles). 
SELECT DISTINCT a.artist_name
FROM artists a
JOIN songs s ON a.artist_id = s.artist_id
WHERE a.artist_id IN (
    SELECT artist_id FROM songs WHERE album_id IS NOT NULL
    INTERSECT
    SELECT artist_id FROM songs WHERE album_id IS NULL
);

--What were the top 10 most highly rated albums (highest average user rating) in the period 1990-1999?
SELECT a.album_name, AVG(r.rating_value) AS average_user_rating
FROM albums a
JOIN ratings r ON a.album_id = r.album_id
WHERE r.rating_date BETWEEN '1990-01-01' AND '1999-12-31'
GROUP BY a.album_id, a.album_name
ORDER BY average_user_rating DESC, a.album_name ASC
LIMIT 10;

--Which were the top 3 most rated genres in the years 1991-1995?
SELECT g.genre_name AS genre_name, COUNT(r.rating_id) AS number_of_song_ratings
FROM genres g
JOIN song_genres sg ON g.genre_id = sg.genre_id
JOIN songs s ON sg.song_id = s.song_id
JOIN ratings r ON s.song_id = r.song_id
WHERE r.rating_date BETWEEN '1991-01-01' AND '1995-12-31'
GROUP BY g.genre_id, g.genre_name
ORDER BY number_of_song_ratings DESC
LIMIT 3;

--Which users have a playlist that has an average song rating of 4.0 or more?
SELECT u.username, p.title AS playlist_title, AVG(song_ratings.avg_rating) AS average_song_rating
FROM users u
JOIN playlists p ON u.user_id = p.user_id
JOIN playlist_songs ps ON p.playlist_id = ps.playlist_id
JOIN (
    SELECT s.song_id, AVG(r.rating_value) AS avg_rating
    FROM songs s
    LEFT JOIN ratings r ON s.song_id = r.song_id
    GROUP BY s.song_id
) song_ratings ON ps.song_id = song_ratings.song_id
GROUP BY u.user_id, u.username, p.playlist_id, p.title
HAVING AVG(song_ratings.avg_rating) >= 4.0;

--Who are the top 5 most engaged users in terms of number of ratings?
SELECT u.username, COUNT(r.rating_id) AS number_of_ratings
FROM users u
JOIN ratings r ON u.user_id = r.user_id
WHERE r.song_id IS NOT NULL OR r.album_id IS NOT NULL
GROUP BY u.user_id, u.username
ORDER BY number_of_ratings DESC
LIMIT 5;

--Find the top 10 most prolific artists in the years 1990-2010?
SELECT a.artist_name, COUNT(s.song_id) AS number_of_songs
FROM artists a
JOIN songs s ON a.artist_id = s.artist_id
WHERE (
    (s.album_id IS NULL AND s.release_date BETWEEN '1990-01-01' AND '2010-12-31') OR
    (s.album_id IS NOT NULL AND s.release_date BETWEEN '1990-01-01' AND '2010-12-31')
)
GROUP BY a.artist_id, a.artist_name
ORDER BY number_of_songs DESC
LIMIT 10;

--Find the top 10 songs that are in most number of playlists
SELECT s.title AS song_title, COUNT(ps.playlist_id) AS number_of_playlists
FROM songs s
JOIN playlist_songs ps ON s.song_id = ps.song_id
GROUP BY s.song_id, s.title
ORDER BY number_of_playlists DESC, s.title ASC
LIMIT 10;

--Find the top 20 most rated singles
SELECT s.title AS song_title, a.artist_name, COUNT(r.rating_id) AS number_of_ratings
FROM songs s
JOIN artists a ON s.artist_id = a.artist_id
JOIN ratings r ON s.song_id = r.song_id
WHERE s.album_id IS NULL
GROUP BY s.song_id, s.title, a.artist_name
ORDER BY number_of_ratings DESC
LIMIT 20;

--Find the names of all artists who discontinued making music after 1993
SELECT a.artist_name
FROM artists a
WHERE a.artist_id NOT IN (
    SELECT DISTINCT artist_id
    FROM songs
    WHERE release_date > '1993-12-31'
)
AND a.artist_id IN (
    SELECT DISTINCT artist_id
    FROM songs
);