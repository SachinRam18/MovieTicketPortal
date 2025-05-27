from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta
from app import app, db
from models import Movie, Showtime, Theater, Admin, Booking
from forms import AdminLoginForm, MovieForm, ShowtimeForm, TheaterForm

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and admin.check_password(form.password.data):
            login_user(admin)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin_dashboard'))
        flash('Invalid username or password', 'danger')
    return render_template('admin/login.html', form=form)

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin_dashboard():
    movies_count = Movie.query.count()
    showtimes_count = Showtime.query.count()
    theaters_count = Theater.query.count()
    
    # Get today's and upcoming bookings
    today = datetime.today().date()
    today_datetime = datetime.combine(today, datetime.min.time())
    
    upcoming_showtimes = Showtime.query.filter(Showtime.start_time >= today_datetime).count()
    recent_bookings = Booking.query.order_by(Booking.booking_time.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                          movies_count=movies_count, 
                          showtimes_count=showtimes_count, 
                          theaters_count=theaters_count,
                          upcoming_showtimes=upcoming_showtimes,
                          recent_bookings=recent_bookings)

@app.route('/admin/movies')
@login_required
def admin_movies():
    movies = Movie.query.all()
    return render_template('admin/movies.html', movies=movies)

@app.route('/admin/movies/add', methods=['GET', 'POST'])
@login_required
def admin_add_movie():
    form = MovieForm()
    if form.validate_on_submit():
        movie = Movie(
            title=form.title.data,
            description=form.description.data,
            duration=form.duration.data,
            genre=form.genre.data,
            image_url=form.image_url.data,
            release_date=form.release_date.data
        )
        db.session.add(movie)
        db.session.commit()
        flash('Movie added successfully!', 'success')
        return redirect(url_for('admin_movies'))
    return render_template('admin/movies.html', form=form)

@app.route('/admin/movies/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    form = MovieForm(obj=movie)
    if form.validate_on_submit():
        movie.title = form.title.data
        movie.description = form.description.data
        movie.duration = form.duration.data
        movie.genre = form.genre.data
        movie.image_url = form.image_url.data
        movie.release_date = form.release_date.data
        db.session.commit()
        flash('Movie updated successfully!', 'success')
        return redirect(url_for('admin_movies'))
    return render_template('admin/movies.html', form=form, movie=movie)

@app.route('/admin/movies/delete/<int:movie_id>', methods=['POST'])
@login_required
def admin_delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Movie deleted successfully!', 'success')
    return redirect(url_for('admin_movies'))

@app.route('/admin/theaters')
@login_required
def admin_theaters():
    theaters = Theater.query.all()
    return render_template('admin/theaters.html', theaters=theaters)

@app.route('/admin/theaters/add', methods=['GET', 'POST'])
@login_required
def admin_add_theater():
    form = TheaterForm()
    if form.validate_on_submit():
        theater = Theater(
            name=form.name.data,
            capacity=form.capacity.data,
            rows=form.rows.data,
            seats_per_row=form.seats_per_row.data
        )
        db.session.add(theater)
        db.session.commit()
        flash('Theater added successfully!', 'success')
        return redirect(url_for('admin_theaters'))
    return render_template('admin/theaters.html', form=form)

@app.route('/admin/theaters/edit/<int:theater_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_theater(theater_id):
    theater = Theater.query.get_or_404(theater_id)
    form = TheaterForm(obj=theater)
    if form.validate_on_submit():
        theater.name = form.name.data
        theater.capacity = form.capacity.data
        theater.rows = form.rows.data
        theater.seats_per_row = form.seats_per_row.data
        db.session.commit()
        flash('Theater updated successfully!', 'success')
        return redirect(url_for('admin_theaters'))
    return render_template('admin/theaters.html', form=form, theater=theater)

@app.route('/admin/theaters/delete/<int:theater_id>', methods=['POST'])
@login_required
def admin_delete_theater(theater_id):
    theater = Theater.query.get_or_404(theater_id)
    db.session.delete(theater)
    db.session.commit()
    flash('Theater deleted successfully!', 'success')
    return redirect(url_for('admin_theaters'))

@app.route('/admin/showtimes')
@login_required
def admin_showtimes():
    showtimes = Showtime.query.all()
    form = ShowtimeForm()
    form.movie_id.choices = [(m.id, m.title) for m in Movie.query.all()]
    form.theater_id.choices = [(t.id, t.name) for t in Theater.query.all()]
    return render_template('admin/showtimes.html', showtimes=showtimes, form=form)

@app.route('/admin/showtimes/add', methods=['GET', 'POST'])
@login_required
def admin_add_showtime():
    form = ShowtimeForm()
    form.movie_id.choices = [(m.id, m.title) for m in Movie.query.all()]
    form.theater_id.choices = [(t.id, t.name) for t in Theater.query.all()]
    
    if form.validate_on_submit():
        showtime = Showtime(
            movie_id=form.movie_id.data,
            theater_id=form.theater_id.data,
            start_time=form.start_time.data,
            price=form.price.data
        )
        db.session.add(showtime)
        db.session.commit()
        flash('Showtime added successfully!', 'success')
        return redirect(url_for('admin_showtimes'))
    return render_template('admin/showtimes.html', form=form)

@app.route('/admin/showtimes/edit/<int:showtime_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_showtime(showtime_id):
    showtime = Showtime.query.get_or_404(showtime_id)
    form = ShowtimeForm(obj=showtime)
    form.movie_id.choices = [(m.id, m.title) for m in Movie.query.all()]
    form.theater_id.choices = [(t.id, t.name) for t in Theater.query.all()]
    
    if form.validate_on_submit():
        showtime.movie_id = form.movie_id.data
        showtime.theater_id = form.theater_id.data
        showtime.start_time = form.start_time.data
        showtime.price = form.price.data
        db.session.commit()
        flash('Showtime updated successfully!', 'success')
        return redirect(url_for('admin_showtimes'))
    return render_template('admin/showtimes.html', form=form, showtime=showtime)

@app.route('/admin/showtimes/delete/<int:showtime_id>', methods=['POST'])
@login_required
def admin_delete_showtime(showtime_id):
    showtime = Showtime.query.get_or_404(showtime_id)
    db.session.delete(showtime)
    db.session.commit()
    flash('Showtime deleted successfully!', 'success')
    return redirect(url_for('admin_showtimes'))
