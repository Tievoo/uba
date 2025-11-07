SELECT ar.Name, COUNT(a.AlbumId) as CantidadAlbumes FROM Artist ar
join Album a on a.ArtistId = ar.ArtistId
GROUP BY ar.Name
HAVING COUNT(a.AlbumId) > 10
ORDER BY CantidadAlbumes DESC;