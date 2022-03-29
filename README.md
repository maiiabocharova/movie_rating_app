## Environment:
- Python version: 3.10
- FastAPI version: 3.0.6

## Read-Only Files:
- app/tests.py

In this challenge, your task is to implement a simple REST API to rate movies. There are two kinds of entities your API must handle: Movies and Ratings.

The definitions and detailed requirements list follow. You will be graded on whether your application performs data retrieval and manipulation based on given use cases exactly as described in the requirements.

## Data

Each movie is a JSON object with the following properties:

- `id`: a unique integer ID of the movie
- `title`: a string denoting the title of the movie
- `rating`: a float denoting the average rating of the movie, calculated from all ratings that were added to the movie. If no such ratings exist, this value is null.

Example of a movie JSON object:

```json
{
   "id": 1,
   "title":"Happy Family",
   "rating": 4.5
}
```

Each rating is a JSON object with the following properties:

- `id`: a unique integer ID of the rating
- `movie`: an integer denoting the movie ID to which the rating was submitted
- `value`: an integer in the range [1-5] denoting the numerical value assigned to the rating

Example of a rating JSON object:

```json
{
   "id": 1,
   "movie": 1,
   "value": 4
}
```

## Requirements

The REST service must expose the `/movies/` and `/ratings/` endpoints, which allow for managing the collection of Movies and Ratings in the following way:

`POST` request to `/movies/`:

- creates a new movie
- expects a body payload containing the title of the movie
- adds the given movie to the collection of movies and assigns a unique integer id to it. The first created movie must have id 1, the second one 2, and so on.
- the response code is 201, and the response body is the created movie object

`GET` request to `/movies/:id/`:

- returns a movie with the given id
- if the matching movie exists, the response code is 200 and the response body is the matching movie object
- if there is no movie with the given id in the collection, the response code is 404

`POST` request to `/ratings/`:

- creates a new rating
- expects a body payload containing movie and value
- if the given movie does not exist, the response code is 404
- if the given movie exists but the rating value is not in the required [1-5] range, then the response code is 400
- if the given movie exists and the rating value is valid, it creates a new rating with the given value related to the given movie and assigns a unique integer id to it. The first created rating must have id 1, the second one 2, and so on.
- if the rating was successfully created, then the response code is 201 and the response body is the created rating object

Your task is to complete the given project so that it passes all the test cases when running the provided unit tests. The implementation of the model is already provided. The project by default supports the use of the SQLite3 database. Implement the `POST` request to `/movies/` first because testing the other methods requires `POST` to work correctly.

## Example requests and responses

`POST` request to `/movies/`

Request body:

```json
{
   "title": "Happy Family"
}
```

The response code is 201, and the response body (when converted to JSON) is:

```json
{
   "id": 1,
   "title": "Happy Family",
   "rating": null
}
```

This adds a new movie with id 1 to the collection of movies.

`POST` request to `/ratings/`

Request body:

```json
{
   "movie": 1,
   "value": 3
}
```

The response code is 201, and the response body (when converted to JSON) is:

```json
{
   "id": 1,
   "movie": 1,
   "value": 3
}
```

This adds to the collection of ratings a new rating with id 1, value 3, and related to the movie with id 1. If the given movie doesn't exist, the response code is 404. If the given movie exists but the rating value is not in the [1-5] range, the response code is 400.

`GET` request to `/movies/1/`

Assuming that the movie with id 1 exists, and has two ratings related to it with values 3 and 4 respectively, then the response code is 200 and the response body (when converted to JSON) is:

```json
{
   "id": 1,
   "title": "Happy Family",
   "rating": 3.5
}
```

If a movie with id 1 doesn't exist, then the response code is 404 and there are no particular requirements for the response body.
