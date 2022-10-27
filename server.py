"""Server for movie ratings app."""

from crypt import methods
from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/login', methods=['post'])
def login():

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)

    if user and user.password == password:
        session['email'] = user.email
        flash('Logged in!')
    else:
        flash('invalid email/password')

    return render_template('homepage.html')


@app.route('/movies')
def all_movies():
    """View all movies."""

    movies = crud.get_movies()

    return render_template("all_movies.html", movies=movies)


@app.route('/movies/<movie_id>')
def show_movie(movie_id):
    """View movie details page."""

    movie = crud.get_movie_by_id(movie_id)
    avg_score = crud.get_avg_rating(movie_id)

    return render_template("movie_details.html", movie=movie, avg_score=avg_score)


@app.route('/movies/<movie_id>', methods=['post'])
def show_movie_post(movie_id):
    """View movie details page."""

    movie = crud.get_movie_by_id(movie_id)
    user = crud.get_user_by_email(session['email'])
    score = int(request.form.get('rate_this'))

    rating = crud.get_movie_rating_by_user(movie, user)

    if rating:
        rating.score = score
    else:
        rating = crud.create_rating(score, movie, user)
        db.session.add(rating)

    db.session.commit()
    flash('Rating submitted')

    avg_score = crud.get_avg_rating(movie_id)

    return render_template("movie_details.html", movie=movie, avg_score=avg_score)


@app.route('/users')
def all_users():
    """View all movies."""

    users = crud.get_users()

    return render_template("all_users.html", users=users)


@app.route('/users', methods=['post'])
def register_user():
    """Create a new user."""

    email = request.form.get('email')
    password = request.form.get('password')

    if crud.get_user_by_email(email):
        flash('email already in use')
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully. Please log in.')

    return render_template('homepage.html')


@app.route('/users/<user_id>')
def show_user(user_id):
    """View movie details page."""

    user = crud.get_user_by_id(user_id)

    return render_template("user_details.html", user=user)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
