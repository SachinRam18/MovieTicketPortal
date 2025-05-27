from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    movies = conn.execute('SELECT * FROM movies').fetchall()
    conn.close()
    return render_template('index.html', movies=movies)

@app.route('/showtimes/<int:movie_id>')
def showtimes(movie_id):
    conn = get_db_connection()
    movie = conn.execute('SELECT * FROM movies WHERE id = ?', (movie_id,)).fetchone()
    showtimes = conn.execute('SELECT * FROM showtimes WHERE movie_id = ?', (movie_id,)).fetchall()
    conn.close()
    return render_template('showtimes.html', movie=movie, showtimes=showtimes)

@app.route('/seats/<int:showtime_id>', methods=['GET', 'POST'])
def seats(showtime_id):
    conn = get_db_connection()
    showtime = conn.execute('SELECT * FROM showtimes WHERE id = ?', (showtime_id,)).fetchone()
    seats = conn.execute('SELECT * FROM seats WHERE showtime_id = ?', (showtime_id,)).fetchall()

    if request.method == 'POST':
        selected_seats = request.form.getlist('seat')
        user_name = request.form['name']

        for seat in selected_seats:
            conn.execute('UPDATE seats SET is_booked = 1 WHERE seat_number = ? AND showtime_id = ?', (seat, showtime_id))
            conn.execute('INSERT INTO bookings (user_name, seat_number, showtime_id, booking_time) VALUES (?, ?, ?, ?)',
                         (user_name, seat, showtime_id, datetime.now()))

        conn.commit()
        conn.close()
        return render_template('ticket.html', seats=selected_seats, user=user_name, showtime=showtime)

    conn.close()
    return render_template('seats.html', seats=seats, showtime=showtime)

if __name__ == '__main__':
    app.run(debug=True)
