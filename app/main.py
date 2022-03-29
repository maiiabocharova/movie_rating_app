from fastapi import FastAPI, HTTPException
from databases import Database
import uvicorn

from models import movies_table, ratings_table, MovieItem, RatingItem

database = Database('sqlite:///app.db')
app = FastAPI()

@app.on_event("startup")
async def startup():
    # connect to db and create a session when the application is starting
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    # disconnect from db and close the session upon closing the application
    await database.disconnect()

@app.get("/ping")
def ping():
    return {
        "description": "The service is up and running."
    }

@app.post("/ratings/")
async def add_rating(rating: RatingItem):
    # check if rating in defined range [1..5]
    if rating.value > 5 or rating.value < 1:
        raise HTTPException(status_code=400, detail="Rating not in defined range")

    # check if movie exists in the db
    query = f"SELECT id FROM movies WHERE id={rating.movie}"
    movie_id = await database.fetch_one(query=query)
    if not movie_id:
        raise HTTPException(status_code=400, detail="Movie does not exist")

    query = ratings_table.insert()
    rating_id = await database.execute(query=query, values={
        "value": rating.value,
        "movie_id": rating.movie
    })
    return {
        "id": rating_id,
        "movie": rating.movie,
        "value": rating.value
    }

@app.post("/movies/")
async def create_movie(movie: MovieItem):
    query = movies_table.insert()
    movie_id = await database.execute(query=query, values=movie.dict())
    return {
        "id": movie_id,
        "title": movie.title,
        "rating": None
    }
@app.get("/movies/{movie_id}")
async def get_movie(movie_id: int):
    query = f"""SELECT movies.id AS id, 
                       movies.title AS title, 
                       AVG(ratings.value) AS rating 
                FROM movies LEFT JOIN ratings ON movies.id = ratings.movie_id
                WHERE movies.id = {movie_id}"""

    obj = await database.fetch_one(query=query)

    if not obj.title:
        raise HTTPException(status_code=404, detail="Item not found")

    return {
       "id": obj.id,
       "title": obj.title,
       "rating": obj.rating
    }

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)