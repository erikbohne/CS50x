SELECT COUNT(title) FROM movies
JOIN ratings ON movie_id = id
WHERE rating = "10.0";