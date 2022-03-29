from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

class MovieItem(BaseModel):
    title: str

class RatingItem(BaseModel):
    value: int
    movie: int

# Create a sqlite engine instance
engine = create_engine("sqlite:///app.db")

# Create a DeclarativeMeta instance
Base = declarative_base()

class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String)

    def __repr__(self):
        return f"<Movie {self.title}>"

class Rating(Base):
    __tablename__ = 'ratings'
    id = Column(Integer, primary_key=True)
    value = Column(Integer)
    movie_id = Column(Integer, ForeignKey('movies.id'))

    def __repr__(self):
        return f"<Rating {self.value} for movie {self.movie_id}>"

movies_table = Movie.__table__
ratings_table = Rating.__table__

Base.metadata.create_all(engine)