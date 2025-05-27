import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # duration in minutes
    genre = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    showtimes = db.relationship('Showtime', backref='movie', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Movie {self.title}>'

class Theater(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    rows = db.Column(db.Integer, nullable=False)  # Number of rows in the theater
    seats_per_row = db.Column(db.Integer, nullable=False)  # Number of seats per row
    showtimes = db.relationship('Showtime', backref='theater', lazy=True)
    
    def __repr__(self):
        return f'<Theater {self.name}>'

class Showtime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    theater_id = db.Column(db.Integer, db.ForeignKey('theater.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float, nullable=False)
    bookings = db.relationship('Booking', backref='showtime', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Showtime {self.start_time} - {self.movie.title if self.movie else "No movie"}>'
    
    @property
    def formatted_date(self):
        return self.start_time.strftime('%A, %B %d, %Y')
    
    @property
    def formatted_time(self):
        return self.start_time.strftime('%I:%M %p')

class Seat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    row = db.Column(db.String(1), nullable=False)  # A, B, C, etc.
    number = db.Column(db.Integer, nullable=False)  # 1, 2, 3, etc.
    
    def __repr__(self):
        return f'<Seat {self.row}{self.number}>'

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    showtime_id = db.Column(db.Integer, db.ForeignKey('showtime.id'), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(100), nullable=False)
    booking_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    booking_reference = db.Column(db.String(10), nullable=False, unique=True)
    seats = db.relationship('Seat', backref='booking', lazy=True, cascade="all, delete-orphan")
    total_price = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f'<Booking {self.booking_reference}>'

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Admin {self.username}>'
