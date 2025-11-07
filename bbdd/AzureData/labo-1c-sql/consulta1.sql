with TotalPerCustomer as (
    SELECT c.FirstName,
    c.LastName,
    SUM(i.Total) as TotalPrice
    From Customer c
    JOIN Invoice i ON c.CustomerId = i.CustomerId
    GROUP BY c.CustomerId, c.FirstName, c.LastName
)
SELECT * from TotalPerCustomer
WHERE TotalPrice > (SELECT AVG(TotalPrice) from TotalPerCustomer)
ORDER BY TotalPrice DESC
GO
