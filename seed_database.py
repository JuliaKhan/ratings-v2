"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

#clear the database
os.system("dropdb ratings")
os.system('createdb ratings')

#recreate the tables
model.connect_to_db(server.app)
model.db.create_all()

with open('data/movies.json') as f:
    movie_data = json.loads(f.read())   #turns str of movies.json into list of dicts

movies_in_db = []

for movie_dict in movie_data:
    movie = crud.create_movie(
        movie_dict['title'],
        movie_dict['overview'],
        #convert date str ('2015-10-31') into datetime type
        datetime.strptime(movie_dict['release_date'],"%Y-%m-%d"),
        movie_dict['poster_path']
    )
    movies_in_db.append(movie)

model.db.session.add_all(movies_in_db)
model.db.session.commit()

for n in range(10):
    email = f'user{n}@test.com'  # Voila! A unique email!
    password = 'test'

    user = crud.create_user(email, password)

    rating = crud.create_rating(
        randint(1,5),
        choice(movies_in_db),
        user
    )

    model.db.session.add(rating)

model.db.session.commit()
