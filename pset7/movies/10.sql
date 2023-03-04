SELECT DISTINCT(name) FROM people
JOIN directors ON people.id = person_id
JOIN ratings ON directors.movie_id = ratings.movie_id
WHERE rating >= "9.0";