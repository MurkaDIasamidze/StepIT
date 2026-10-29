
-- 1. Create Table (books)

CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    author VARCHAR(100) NOT NULL,
    genre VARCHAR(50),
    publish_year INTEGER,
    pages INTEGER,
    price NUMERIC(8,2)
);


-- 2. Insert at least 15 records

INSERT INTO books (title, author, genre, publish_year, pages, price) VALUES
('The Hobbit', 'J.R.R. Tolkien', 'Fantasy', 1937, 310, 25.50),
('Harry Potter and the Sorcerer''s Stone', 'J.K. Rowling', 'Fantasy', 1997, 309, 35.00),
('1984', 'George Orwell', 'Dystopian', 1949, 328, 18.00),
('The Great Gatsby', 'F. Scott Fitzgerald', 'Classic', 1925, 180, 15.00),
('To Kill a Mockingbird', 'Harper Lee', 'Fiction', 1960, 281, 22.00),
('Project Hail Mary', 'Andy Weir', 'Sci-Fi', 2021, 496, 42.00),
('Dune', 'Frank Herbert', 'Sci-Fi', 1965, 412, 38.50),
('Atomic Habits', 'James Clear', 'Self-Help', 2018, 320, 29.90),
('The Midnight Library', 'Matt Haig', 'Fantasy', 2020, 304, 31.00),
('Klara and the Sun', 'Kazuo Ishiguro', 'Sci-Fi', 2021, 303, 34.00),
('The Catcher in the Rye', 'J.D. Salinger', 'Classic', 1951, 234, 16.50),
('Brave New World', 'Aldous Huxley', 'Dystopian', 1932, 288, 19.00),
('Fahrenheit 451', 'Ray Bradbury', 'Dystopian', 1953, 256, 21.00),
('The Lord of the Rings', 'J.R.R. Tolkien', 'Fantasy', 1954, 1178, 65.00),
('Fourth Wing', 'Rebecca Yarros', 'Fantasy', 2023, 528, 45.00);


-- 3. SELECT Queries


-- 3.1 All books
SELECT * FROM books;

-- 3.2 Only book title and author
SELECT title, author FROM books;

-- 3.3 All books with price greater than 30
SELECT * FROM books WHERE price > 30;

-- 3.4 All books published in 2020 or later
SELECT * FROM books WHERE publish_year >= 2020;

-- 3.5 All books with genre "Fantasy"
SELECT * FROM books WHERE genre = 'Fantasy';

-- 3.6 All books with page count greater than 300
SELECT * FROM books WHERE pages > 300;

-- 3.7 All books ordered by price ascending
SELECT * FROM books ORDER BY price ASC;

-- 3.8 All books ordered by publish year descending
SELECT * FROM books ORDER BY publish_year DESC;

-- ==========================================
-- 4. Update Data (UPDATE)
-- ==========================================

-- 4.1 Update the price of one book (e.g., id = 1)
UPDATE books SET price = 28.00 WHERE id = 1;

-- 4.2 Update the genre of one book (e.g., id = 3)
UPDATE books SET genre = 'Science Fiction' WHERE id = 3;

-- 4.3 Update the page count of one book (e.g., id = 4)
UPDATE books SET pages = 200 WHERE id = 4;


-- 5. Delete Data (DELETE)


-- 5.1 Delete one specific book (e.g., id = 5)
DELETE FROM books WHERE id = 5;

-- 5.2 Delete all books published before 2000
DELETE FROM books WHERE publish_year < 2000;


-- 6. Add 5 Additional Books

INSERT INTO books (title, author, genre, publish_year, pages, price) VALUES
('Demon Copperhead', 'Barbara Kingsolver', 'Fiction', 2022, 560, 39.00),
('Tomorrow, and Tomorrow, and Tomorrow', 'Gabrielle Zevin', 'Fiction', 2022, 416, 33.50),
('House of Sky and Breath', 'Sarah J. Maas', 'Fantasy', 2022, 800, 48.00),
('Yellowface', 'R.F. Kuang', 'Drama', 2023, 336, 30.00),
('Iron Flame', 'Rebecca Yarros', 'Fantasy', 2023, 624, 46.00);

-- 7. Final Check

SELECT * FROM books;


-- 8. Drop Table
-- (Run this ONLY after you have taken all required screenshots!)

DROP TABLE books;