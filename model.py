from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, relationship, backref

### Variable Definitions 

ENGINE = None
Session = None 
Base = declarative_base()

### Class declarations go here

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable=True)
    password = Column(String(64), nullable=True)
    age = Column(Integer, nullable=True)
    zipcode = Column(String(15), nullable=True)
    

class Ratings(Base): 
    __tablename__ = "ratings"
    rating_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    movie_id = Column(Integer, ForeignKey('Movies.movie_id'))
    rating = Column(Integer)
    timestamp = Column(DateTime)
    user = relationship("User", backref=backref("ratings", order_by=rating_id))
    movie = relationship("Movie")

class Movie(Base):
    __tablename__ = "Movies"
    movie_id = Column(Integer, primary_key = True)
    movie_title = Column(String(200))
    release_date = Column(DateTime, nullable=True)
    imdb_url = Column(String(200), nullable=True)
    ratings = relationship("Ratings")

### End class declarations

### Query functions: ADD 

def add_user(session, email, password):
    new_user = User(email=email, password=password)
    session.add(new_user)
    session.commit()

def add_rating(session, movie_id, rating, user_id):
    movie = get_movie_by_id(session=session, movie_id = movie_id)
    new_rating = Ratings(user_id=user_id, movie_id=movie_id, rating=rating)
    movie.ratings.append(new_rating) 
    session.commit()

### Query functions: GET

def get_movie_by_id(session, movie_id):
     movie = session.query(Movie).filter_by(movie_id=movie_id).first()
     return movie

def get_movies_by_user(session, user_id):
    ratings = session.query(Ratings).filter_by(user_id=user_id).all()
    movies = []
    for rating in ratings: 
        movie = session.query(Movie).filter_by(movie_id=rating.movie_id).first()
        movies.append(movie)
    return movies

# def get_movie_by_ids(session, movie_id, user_id):
#     movie = session.query(Movie).filter_by(movie_id=movie_id).first()
#     return movie

def get_users(session):
    user_objects = session.query(User).all()
    return user_objects #We just changed this. 

### Query functions: verify 

def verify_user(session, email, passw):
    user = session.query(User).filter_by(email=email).first()
    if user.password == passw:
        return user       
    else: 
        return None 

### Main functions 

def main():
    """In case we need this for something"""
    pass

def connect():
    global ENGINE
    global Session
    ENGINE = create_engine("sqlite:///ratings.db", echo=True)
    Session = sessionmaker(bind=ENGINE)
    return Session()

if __name__ == "__main__":
    main()
