-- Create Movies Table
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    image_url TEXT
);

-- Insert some sample movies
INSERT INTO movies (title, description, image_url) VALUES
('Inception', 'A mind-bending thriller', 'inception.jpg'),
('Interstellar', 'A journey across time and space', 'interstellar.jpg'),
('The Dark Knight', 'Batman vs Joker', 'darkknight.jpg');

-- Create Showtimes Table
CREATE TABLE IF NOT EXISTS showtimes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_id INTEGER,
    show_time TEXT,
    FOREIGN KEY(movie_id) REFERENCES movies(id)
);

-- Sample Showtimes
INSERT INTO showtimes (movie_id, show_time) VALUES
(1, '2025-05-26 18:00'),
(1, '2025-05-26 21:00'),
(2, '2025-05-27 17:30'),
(3, '2025-05-28 20:00');

-- Create Seats Table
CREATE TABLE IF NOT EXISTS seats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    showtime_id INTEGER,
    seat_number TEXT,
    is_booked INTEGER DEFAULT 0,
    FOREIGN KEY(showtime_id) REFERENCES showtimes(id)
);

-- Generate 20 seats per showtime
INSERT INTO seats (showtime_id, seat_number)
SELECT s.id, 'A' || n
FROM showtimes s,
     (SELECT 1 as n UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5
      UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10
      UNION ALL SELECT 11 UNION ALL SELECT 12 UNION ALL SELECT 13 UNION ALL SELECT 14 UNION ALL SELECT 15
      UNION ALL SELECT 16 UNION ALL SELECT 17 UNION ALL SELECT 18 UNION ALL SELECT 19 UNION ALL SELECT 20) nums;

-- Create Bookings Table
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT,
    seat_number TEXT,
    showtime_id INTEGER,
    booking_time TEXT,
    FOREIGN KEY(showtime_id) REFERENCES showtimes(id)
);
