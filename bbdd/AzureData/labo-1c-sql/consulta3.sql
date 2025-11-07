WITH AvgTrackDuration AS (
    SELECT AVG(t.Milliseconds) as SongAvg FROM Track t
)
SELECT A.Title from Album A
join Track t on t.AlbumId = a.AlbumId
WHERE NOT EXISTS (
    SELECT 1
    FROM Track t2
    WHERE t2.AlbumId = t.AlbumId
    AND t2.Milliseconds < (SELECT SongAvg from AvgTrackDuration)
)
GROUP BY A.Title
ORDER BY A.Title ASC
