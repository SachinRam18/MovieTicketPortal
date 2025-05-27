from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, PasswordField, FloatField, DateField, DateTimeLocalField
from wtforms.validators import DataRequired, Email, Length, NumberRange

class BookingForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])

class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class MovieForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    duration = IntegerField('Duration (minutes)', validators=[DataRequired(), NumberRange(min=1)])
    genre = StringField('Genre', validators=[DataRequired(), Length(max=50)])
    image_url = StringField('Image URL', validators=[DataRequired(), Length(max=255)])
    release_date = DateField('Release Date', validators=[DataRequired()])

class TheaterForm(FlaskForm):
    name = StringField('Theater Name', validators=[DataRequired(), Length(max=50)])
    capacity = IntegerField('Capacity', validators=[DataRequired(), NumberRange(min=1)])
    rows = IntegerField('Number of Rows', validators=[DataRequired(), NumberRange(min=1, max=26)])
    seats_per_row = IntegerField('Seats per Row', validators=[DataRequired(), NumberRange(min=1)])

class ShowtimeForm(FlaskForm):
    movie_id = SelectField('Movie', coerce=int, validators=[DataRequired()])
    theater_id = SelectField('Theater', coerce=int, validators=[DataRequired()])
    start_time = DateTimeLocalField('Start Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    price = FloatField('Ticket Price', validators=[DataRequired(), NumberRange(min=0.01)])
