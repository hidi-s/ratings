import model
import csv
from datetime import date
import time

def load_users(session):
    with open("seed_data/u.user", "rb") as f:
        reader = csv.reader(f)
        for row in reader:
            data = row[0].split("|")
            id = data[0]
            zipcode = data[4]
            new_user = model.User(id = id, zipcode = zipcode)
            session.add(new_user)
        session.commit()
        f.close()

def load_movies(session):
    with open ("seed_data/u.item", "rb") as f:
        reader = csv.reader(f,delimiter='\n')
        for row in reader: 
            data = row[0].split("|")
            movie_id = data[0]
            movie_title = data[1]
            movie_title = movie_title.decode("latin-1")
            if data[4] != "":
                imdb_url = data[4]
            else:
                imdb_url = None 
            if data[2] != "":
                rdate = time.strptime(data[2],"%d-%b-%Y")
                release_date = date(rdate[0],rdate[1],rdate[2])
            else:
                release_date = None 
            new_movie = model.Movie(movie_id = movie_id, movie_title=movie_title, release_date=release_date, imdb_url=imdb_url)      
            session.add(new_movie)
        session.commit()
        f.close()

def load_ratings(session):
    with open ("seed_data/u.data", "rb") as f:
        reader = csv.reader(f)
        for row in reader:
            data = row[0].split()
            user_id = data[0]
            movie_id = data[1]
            rating = data[2]
            timestamp = date.fromtimestamp(float(data[3]))
            new_rating = model.Ratings(user_id=user_id, movie_id=movie_id, rating=rating, timestamp=timestamp)
            session.add(new_rating)
        session.commit()
        f.close()

def main(session):
    load_movies(session)
    load_users(session)
    load_ratings(session)

if __name__ == "__main__":
    s= model.connect()
    main(s)
