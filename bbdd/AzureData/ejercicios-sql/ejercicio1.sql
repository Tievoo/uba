SELECT t.Name, g.Name as Genre, m.name as MediaType FROM Track t
JOIN Genre g ON g.GenreId = t.GenreId
JOIN MediaType m on t.MediaTypeId = m.MediaTypeId
