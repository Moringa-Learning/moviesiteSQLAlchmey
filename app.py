from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Sequence, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Define the database connection
DATABASE_URI = 'sqlite:///movies.db' # the path to the database
engine = create_engine(DATABASE_URI, echo=True)

# base class for all the classes
Base = declarative_base()

class Director(Base):
    __tablename__ = 'director'
    dir_id = Column(Integer, Sequence('dir_id_seq'), primary_key=True)
    dir_name = Column(String)
    dir_experience = Column(Integer)

    movie = relationship('Movie', back_populates='director')

class Movie(Base):
    __tablename__ = 'movie'
    movie_id = Column(Integer, Sequence('movie_id_seq'), primary_key=True)
    movie_title = Column(String)
    movie_plot = Column(String)
    movie_genre = Column(String)
    director_id = Column(Integer, ForeignKey('director.dir_id'))

    director = relationship('Director', back_populates='movie') # one to One Relationship
    movie_cast = relationship('Cast', back_populates='movies') 

class Actor(Base):
    __tablename__ = 'actor'
    actor_id = Column(Integer, Sequence('actor_id_seq'), primary_key=True)
    actor_name = Column(String(255))
    actor_gender = Column(String(255))
    actor_salary = Column(Integer)

    cast = relationship("Cast", back_populates='actors')

class Cast(Base):
    __tablename__ = 'cast'
    cast_id = Column(Integer, Sequence('cast_id_seq'), primary_key=True)
    actor_id = Column(Integer, ForeignKey('actor.actor_id'))
    movie_id = Column(Integer, ForeignKey('movie.movie_id'))

    actors = relationship('Actor', back_populates='cast')
    movies = relationship('Movie', back_populates='movie_cast')

# creating all the tables
Base.metadata.create_all(bind=engine)

# create session
Session = sessionmaker(bind=engine)
session = Session()

# # Insert Data
# # ---- Director 
# dir1 = Director(dir_name='Zack Snyder', dir_experience=10)
# dir2 =  Director(dir_name='George Okumu', dir_experience=5)
# session.add(dir1)
# session.add(dir2)

# session.commit()

# # -- actors
# actor1 = Actor(actor_name='Maingi Samuel', actor_gender='Male', actor_salary=60000000)
# actor2 = Actor(actor_name='Natalie Wanjiru', actor_gender='Female', actor_salary=80000000)
# actor3 = Actor(actor_name='Abdihakim Hassan', actor_gender='Male', actor_salary=100000000)

# session.add_all([actor1, actor2, actor3])
# session.commit()

# # -- movie
# movie1 = Movie(movie_title='Justice League', movie_plot='Loremjshasajsdk djsjjhsdhsd', movie_genre='Action', director_id=dir1.dir_id)
# session.add(movie1)
# session.commit()

# # -- cast
# cast1 = Cast(actor_id=actor1.actor_id, movie_id=movie1.movie_id)
# cast2 = Cast(actor_id=actor2.actor_id, movie_id=movie1.movie_id)
# session.add_all([cast1, cast2])
# session.commit()

# -- get data Actors
# all_actors = session.query(Actor).all()
# print(all_actors)

# for actor in all_actors:
#     print(actor.actor_name)

# ---- get movie
one_movie = session.query(Movie).filter_by(movie_id = 1).first()
print(one_movie.director.dir_name, '*'*40)

session.close()