-- Consulta A
SELECT * FROM Sales.SalesOrderDetail d
JOIN Production.Product p ON d.ProductID = p.ProductID;
-- Consulta B
SELECT * FROM Sales.SalesOrderDetail d
JOIN Production.Product p ON d.ProductID = p.ProductID
WHERE p.Name LIKE 'A%';
