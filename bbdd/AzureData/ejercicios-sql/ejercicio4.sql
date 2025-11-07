SELECT ar.Name, COUNT(t.TrackId) as Count FROM Artist ar
JOIN Album a on a.ArtistId = ar.ArtistId
JOIN Track t on t.AlbumId = a.AlbumId
GROUP BY ar.ArtistId, ar.Name
HAVING COUNT(t.TrackId) > 50
ORDER BY COUNT(T.TrackId) DESC