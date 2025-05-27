from datetime import datetime, timedelta
import random
from app import app, db
from models import Movie, Theater, Showtime

def add_showtimes():
    with app.app_context():
        # Clear existing showtimes
        db.session.query(Showtime).delete()
        db.session.commit()
        
        # Get movies and theaters
        movies = Movie.query.all()
        theaters = Theater.query.all()
        
        if not movies or not theaters:
            print("No movies or theaters found in database.")
            return
        
        # Add showtimes for the next 7 days
        now = datetime.now()
        start_date = datetime(now.year, now.month, now.day)
        
        print(f"Adding showtimes for {len(movies)} movies in {len(theaters)} theaters...")
        
        showtimes_added = 0
        
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
                        showtimes_added += 1
        
        db.session.commit()
        print(f"Successfully added {showtimes_added} showtimes!")

if __name__ == "__main__":
    try:
        add_showtimes()
    except Exception as e:
        print(f"Error adding showtimes: {e}")