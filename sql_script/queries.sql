
-- Average price for each rating

SELECT Rating,
       COUNT(*) AS BooksCount,
       CAST(AVG(Price) AS DECIMAL(10,2))  AS AvgPrice
FROM Books
GROUP BY Rating
ORDER BY Rating;



-- The 5 most expensive books rated 4 or 5

SELECT TOP (5) Title, Price, Rating
FROM Books
WHERE Rating IN (4, 5)
ORDER BY Price DESC;


--How many books are out of stock, per rating

SELECT Rating,
       SUM(CASE WHEN InStock = 0 THEN 1 ELSE 0 END) AS OutOfStockCount
FROM dbo.Books
GROUP BY Rating
ORDER BY Rating;
