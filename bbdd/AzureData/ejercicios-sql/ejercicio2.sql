SELECT g.Name, COUNT(t.TrackId) as Count FROM Genre g
LEFT JOIN Track t on t.GenreId = g.GenreId
GROUP BY g.Name
ORDER BY Count DESC