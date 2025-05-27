from datetime import datetime, timedelta
import random
from app import app, db
from models import Movie, Theater, Showtime, Admin
from werkzeug.security import generate_password_hash

def initialize_database():
    with app.app_context():
        # Clear existing data
        db.session.query(Showtime).delete()
        db.session.query(Movie).delete()
        db.session.query(Theater).delete()
        db.session.query(Admin).delete()
        db.session.commit()
        
        # Create admin user
        admin = Admin(
            username="admin",
            email="admin@cinema.com"
        )
        admin.set_password("admin123")
        db.session.add(admin)
        
        # Add sample movies
        movies = [
            Movie(
                title="Inception",
                description="A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
                duration=148,
                genre="Sci-Fi, Action",
                image_url="https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_.jpg",
                release_date=datetime(2010, 7, 16).date()
            ),
            Movie(
                title="The Dark Knight",
                description="When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
                duration=152,
                genre="Action, Crime, Drama",
                image_url="https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_.jpg",
                release_date=datetime(2008, 7, 18).date()
            ),
            Movie(
                title="Interstellar",
                description="A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
                duration=169,
                genre="Adventure, Drama, Sci-Fi",
                image_url="https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg",
                release_date=datetime(2014, 11, 7).date()
            ),
            Movie(
                title="Pulp Fiction",
                description="The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
                duration=154,
                genre="Crime, Drama",
                image_url="https://m.media-amazon.com/images/M/MV5BNGNhMDIzZTUtNTBlZi00MTRlLWFjM2ItYzViMjE3YzI5MjljXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg",
                release_date=datetime(1994, 10, 14).date()
            ),
            Movie(
                title="The Matrix",
                description="A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
                duration=136,
                genre="Action, Sci-Fi",
                image_url="https://m.media-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNkYzNjNTc4L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg",
                release_date=datetime(1999, 3, 31).date()
            )
        ]
        
        for movie in movies:
            db.session.add(movie)
        
        # Add theaters
        theaters = [
            Theater(name="Main Hall", capacity=120, rows=10, seats_per_row=12),
            Theater(name="VIP Theater", capacity=60, rows=6, seats_per_row=10),
            Theater(name="IMAX Experience", capacity=200, rows=10, seats_per_row=20)
        ]
        
        for theater in theaters:
            db.session.add(theater)
        
        db.session.commit()
        
        # Add showtimes for the next 7 days
        now = datetime.now()
        start_date = datetime(now.year, now.month, now.day)
        
        for day in range(7):
            current_date = start_date + timedelta(days=day)
            
            # Morning, afternoon, and evening showtimes
            showtime_slots = [
                current_date + timedelta(hours=10, minutes=30),
                current_date + timedelta(hours=13, minutes=15),
                current_date + timedelta(hours=16, minutes=0),
                current_date + timedelta(hours=19, minutes=30),
                current_date + timedelta(hours=22, minutes=0)
            ]
            
            # Create showtimes for each movie in different theaters and time slots
            for movie in movies:
                # Each movie gets 3 random showtimes over the week
                for _ in range(3):
                    theater = random.choice(theaters)
                    showtime_datetime = random.choice(showtime_slots)
                    
                    # Avoid duplicate showtimes in the same theater
                    existing = Showtime.query.filter_by(
                        theater_id=theater.id, 
                        start_time=showtime_datetime
                    ).first()
                    
                    if not existing:
                        price = 12.99 if theater.name == "Main Hall" else (
                            19.99 if theater.name == "VIP Theater" else 16.99
                        )
                        
                        showtime = Showtime(
                            movie_id=movie.id,
                            theater_id=theater.id,
                            start_time=showtime_datetime,
                            price=price
                        )
                        db.session.add(showtime)
        
        db.session.commit()
        print("Database initialized with sample data!")

if __name__ == "__main__":
    try:
        print("Starting database initialization...")
        initialize_database()
        print("Database initialization completed successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
