import random
import string
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, jsonify, abort
from app import app, db
from models import Movie, Showtime, Booking, Seat, Theater
from forms import BookingForm

@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

@app.route('/movie/<int:movie_id>/showtimes')
def showtimes(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    showtimes = Showtime.query.filter_by(movie_id=movie_id).order_by(Showtime.start_time).all()
    return render_template('showtimes.html', movie=movie, showtimes=showtimes)

@app.route('/showtime/<int:showtime_id>/seats')
def seats(showtime_id):
    showtime = Showtime.query.get_or_404(showtime_id)
    
    # Get all booked seats for this showtime
    booked_seats = []
    bookings = Booking.query.filter_by(showtime_id=showtime_id).all()
    for booking in bookings:
        seats = Seat.query.filter_by(booking_id=booking.id).all()
        for seat in seats:
            booked_seats.append(f"{seat.row}{seat.number}")
    
    return render_template('seats.html', showtime=showtime, booked_seats=booked_seats)

@app.route('/showtime/<int:showtime_id>/book', methods=['GET', 'POST'])
def book(showtime_id):
    showtime = Showtime.query.get_or_404(showtime_id)
    selected_seats = request.args.get('seats', '')
    
    if not selected_seats:
        flash('Please select at least one seat.', 'danger')
        return redirect(url_for('seats', showtime_id=showtime_id))
    
    form = BookingForm()
    
    seats_list = selected_seats.split(',')
    total_price = len(seats_list) * showtime.price
    
    if form.validate_on_submit():
        # Create a random booking reference
        booking_ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        
        # Create a new booking
        booking = Booking(
            showtime_id=showtime_id,
            customer_name=form.name.data,
            customer_email=form.email.data,
            booking_reference=booking_ref,
            total_price=total_price
        )
        db.session.add(booking)
        db.session.flush()  # Get the booking ID without committing
        
        # Create seat records
        for seat_code in seats_list:
            row = seat_code[0]
            number = int(seat_code[1:])
            seat = Seat(booking_id=booking.id, row=row, number=number)
            db.session.add(seat)
        
        db.session.commit()
        
        return redirect(url_for('ticket', booking_ref=booking_ref))
    
    return render_template('book.html', showtime=showtime, selected_seats=selected_seats, 
                          total_price=total_price, form=form, seats_list=seats_list)

@app.route('/ticket/<booking_ref>')
def ticket(booking_ref):
    booking = Booking.query.filter_by(booking_reference=booking_ref).first_or_404()
    seats = Seat.query.filter_by(booking_id=booking.id).all()
    
    seat_list = [f"{seat.row}{seat.number}" for seat in seats]
    seat_str = ", ".join(seat_list)
    
    return render_template('ticket.html', booking=booking, seat_str=seat_str)

@app.route('/api/get-booked-seats/<int:showtime_id>')
def get_booked_seats(showtime_id):
    # Get all booked seats for this showtime
    booked_seats = []
    bookings = Booking.query.filter_by(showtime_id=showtime_id).all()
    for booking in bookings:
        seats = Seat.query.filter_by(booking_id=booking.id).all()
        for seat in seats:
            booked_seats.append(f"{seat.row}{seat.number}")
    
    return jsonify({"booked_seats": booked_seats})

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
