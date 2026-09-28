CREATE TABLE BooksRaw (
    title    NVARCHAR(300),
    price    NVARCHAR(20),
    rating   NVARCHAR(5),
    in_stock NVARCHAR(5),
    url      NVARCHAR(500)
);

BULK INSERT BooksRaw
FROM 'D:\work tasks\books.csv'
WITH (
    FORMAT     = 'CSV',     
    FIRSTROW   = 2,        
    FIELDQUOTE = '"',
    CODEPAGE   = '65001'    
);

CREATE TABLE Books (
    BookID  INT IDENTITY(1,1) PRIMARY KEY,
    Title   NVARCHAR(300) NOT NULL,
    Price   DECIMAL(10,2) NOT NULL,
    Rating  TINYINT       NOT NULL,
    InStock BIT           NOT NULL,
    Url     NVARCHAR(500) NOT NULL
);


INSERT INTO dbo.Books (Title, Price, Rating, InStock, Url)
SELECT title,
       CAST(price AS DECIMAL(10,2)),
       CAST(rating AS TINYINT),
       CASE WHEN in_stock = 'true' THEN 1 ELSE 0 END,
       url
FROM BooksRaw;



SELECT COUNT(*) AS TotalBooks FROM dbo.Books;