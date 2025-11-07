SELECT c.FirstName, c.LastName, COUNT(DISTINCT t.GenreId) as CantidadGeneros FROM Customer c
join Invoice i on i.CustomerId = c.CustomerId
join InvoiceLine il on il.InvoiceId = i.InvoiceID
join Track t on il.TrackId = t.TrackId
GROUP BY c.CustomerId, c.FirstName, c.LastName
having COUNT(DISTINCT t.GenreId) > 1
ORDER BY CantidadGeneros DESC 

