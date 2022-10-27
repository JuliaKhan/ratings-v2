"""CRUD operations."""

from model import db, User, Movie, Rating, connect_to_db

#Functions start here


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)


    return user


def create_movie(title, overview, release_date, poster_path):
    """Create and return a new movie."""

    movie = Movie(title=title, overview=overview,
                release_date=release_date, poster_path=poster_path)
    return movie


def create_rating(score, movie, user):
    """Create and return a new rating"""

    rating = Rating(score=score, movie=movie, user=user)

    return rating


def get_movies():
    """Return a list of all movies."""

    return Movie.query.all()


def get_movie_by_id(movie_id):
    """Return a movie by its id"""

    return Movie.query.filter_by(movie_id=movie_id).one()


def get_users():
    """Return a list of all users."""

    return User.query.all()


def get_user_by_id(user_id):
    """Return a user by their id"""

    return User.query.filter_by(user_id=user_id).one()


def get_user_by_email(email):
    """Return a user by their email"""

    return User.query.filter_by(email=email).first()


def get_movie_rating_by_user(movie, user):
    """Returns the movie's rating submitted by user"""

    return Rating.query.filter(Rating.movie==movie, Rating.user==user).first()


def get_avg_rating(movie_id):
    """Return mean rating for the selected movie"""

    movie = get_movie_by_id(movie_id)
    ratings = movie.ratings
    count_ratings = len(ratings)

    sum_ratings = 0
    for rating in ratings:
        sum_ratings += int(rating.score)
    
    if count_ratings == 0:
        return 'No ratings'
    else:
        return f'{(sum_ratings / count_ratings):.2f}'
    

if __name__ == '__main__':
    from server import app
    connect_to_db(app)