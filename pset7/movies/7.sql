SELECT title, ratings.rating FROM ratings
JOIN movies ON ratings.movie_id = movies.id
WHERE rating >= "1.0" AND year = "2010"
ORDER BY rating DESC, title;