SELECT DISTINCT(title) FROM movies
JOIN stars ON movies.id = stars.movie_id
JOIN people ON stars.person_id = people.id
WHERE stars.movie_id IN (
SELECT movie_id FROM stars
JOIN people ON stars.person_id = people.id
WHERE name = "Helena Bonham Carter")
AND stars.movie_id IN (
SELECT movie_id FROM stars
JOIN people ON stars.person_id = people.id
WHERE name = "Johnny Depp");
