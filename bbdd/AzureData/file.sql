-- Guia de SQL
-- 2.1
-- a)
SELECT FirstName, LastName FROM
Customer WHERE Country = 'Brazil';

-- b)
SELECT C.FirstName, C.LastName, I.InvoiceDate, I.InvoiceID
FROM Invoice I
JOIN Customer C ON C.CustomerID = I.CustomerID;

-- c)
SELECT T.TrackID, T.Name, Ar.Name As ArtistName, Al.Title As AlbumTitle
FROM Track T
JOIN Album Al ON T.AlbumID = Al.AlbumID
JOIN Artist Ar ON Al.ArtistID = Ar.ArtistID;

-- e)
SELECT P.PlaylistId, P.Name, COUNT (t.TrackId) as Count from Playlist P
join PlaylistTrack PT on PT.PlaylistId = P.PlaylistId
join Track t on t.TrackId = Pt.TrackId
join Album A on a.AlbumId = t.AlbumId
join Artist ar on ar.ArtistId = A.ArtistId
WHERE ar.Name = 'Iron Maiden'
GROUP BY P.PlaylistId, P.Name
HAVING COUNT (t.TrackId) > 10;

-- f)
SELECT P.Name, COUNT(DISTINCT t.AlbumId) as AlbumCount FROM Playlist P
join PlaylistTrack pt on pt.PlaylistId = P.PlaylistId
join Track t on t.TrackId = pt.TrackId
GROUP BY P.Name;


-- g)
SELECT E.FirstName, E.LastName from Employee E
JOIN Customer C on C.SupportRepId = E.EmployeeId
join Invoice I on I.CustomerId = C.CustomerId
join InvoiceLine IL on IL.InvoiceId = I.InvoiceId
WHERE DATEDIFF(YEAR, E.BirthDate, GETDATE()) > 25
GROUP BY E.FirstName, E.LastName
HAVING COUNT(IL.InvoiceLineId) > 10

-- h)
SELECT C.FirstName, C.LastName, I.InvoiceDate, I.InvoiceID
FROM Customer C
LEFT OUTER JOIN Invoice I ON C.CustomerID = I.CustomerID;

-- i)
SELECT E.FirstName, E.LastName FROM Employee E
join Customer C on C.SupportRepId = E.EmployeeId
join Invoice I on I.CustomerId = C.CustomerId
GROUP BY E.FirstName, E.LastName
HAVING COUNT(I.InvoiceId) > 10

-- j)
SELECT
    E.FirstName as EmployeeName,
    E.LastName as EmployeeLastName,
    B.FirstName as BossName,
    B.LastName as BossLastName
FROM Employee E
join Employee B on E.ReportsTo = B.EmployeeId
ORDER BY EmployeeName, EmployeeLastName;

-- k)
SELECT
    E.FirstName as EmployeeName,
    E.LastName as EmployeeLastName,
    B.FirstName as BossName,
    B.LastName as BossLastName
FROM Employee E
LEFT join Employee B on E.ReportsTo = B.EmployeeId
ORDER BY EmployeeName, EmployeeLastName;

--l)
SELECT C.FirstName, C.LastName,
    AVG(TracksPorFactura.CantTracks) AS PromedioTracks
FROM Customer C
JOIN (
    SELECT 
        I.CustomerId,
        I.InvoiceId,
        COUNT(IL.InvoiceLineId) AS CantTracks
    FROM Invoice I
    JOIN InvoiceLine IL ON IL.InvoiceId = I.InvoiceId
    GROUP BY I.CustomerId, I.InvoiceId
) AS TracksPorFactura 
    ON TracksPorFactura.CustomerId = C.CustomerId
GROUP BY C.CustomerId, C.FirstName, C.LastName
ORDER BY PromedioTracks DESC;

SELECT * From Genre;

-- m)
SELECT E.FirstName, E.LastName, SUM(RockTracksPerCustomer.Amount) as Amount  from Employee E
join Customer C on C.SupportRepId = E.EmployeeId
JOIN (
    SELECT
        I.CustomerId,
        COUNT(t.TrackId) AS Amount
    FROM Invoice I
    JOIN InvoiceLine IL on IL.InvoiceId = I.InvoiceId
    JOIN Track t on t.TrackId = Il.TrackId
    JOIN Genre g on t.GenreId = g.GenreId
    WHERE g.Name = 'Rock'
    GROUP BY I.CustomerId
) AS RockTracksPerCustomer ON RockTracksPerCustomer.CustomerId = C.CustomerId
GROUP By E.FirstName, E.LastName;

-- 2.3)
-- a)
WITH TotalPlaylists AS (
  SELECT COUNT(PlaylistId) AS Total FROM Playlist
)
SELECT a.AlbumId, a.Title
FROM Album a
JOIN Track t ON t.AlbumId = a.AlbumId
JOIN PlaylistTrack pt ON pt.TrackId = t.TrackId
GROUP BY a.AlbumId, a.Title
HAVING COUNT(DISTINCT pt.PlaylistId) = (SELECT Total FROM TotalPlaylists);

