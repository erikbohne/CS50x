SELECT DISTINCT(name) FROM people
JOIN stars ON people.id = person_id
JOIN movies ON stars.movie_id = movies.id
WHERE year = "2004"
ORDER BY birth;