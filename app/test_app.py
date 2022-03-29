from fastapi.testclient import TestClient
from main import app
import json
import asyncio
from delete_records import delete_records
client = TestClient(app)

# healthcheck
def test_healthcheck():
    response = client.get("/ping")
    assert response.status_code == 200

movie_payload = {
    'title': 'Happy Family',
}
# delete all recored from table
def test_delete_records():
    asyncio.run(delete_records())

'''#############################
#####  CreateMovieTestCase  #####
#################################'''
def test_with_valid_payload():
    response = client.post("/movies/", data=json.dumps(movie_payload))
    assert response.status_code == 200
    expected_movie = {
            'id': 1,
            'title': movie_payload['title'],
            'rating': None,
        }
    assert response.json() == expected_movie

def test_with_existing_movie():
        rating_payload = {
            'movie': 1,
            'value': 4,
        }
        response = client.post('/ratings/', data=json.dumps(rating_payload))
        assert response.status_code == 200
        expected_rating = {
            'id': 1,
            'movie': 1,
            'value': 4,
        }
        assert response.json() == expected_rating

'''#############################
#####  AddRatingTestCase  #####
#################################'''

def test_with_rating_smaller_than_allowed_minimum():
    rating_payload = {
        'movie': 1,
        'value': 0,
    }
    response = client.post('/ratings/', data=json.dumps(rating_payload))
    assert response.status_code == 400

def test_with_rating_greater_than_allowed_maximum():
    rating_payload = {
        'movie': 1,
        'value': 6,
    }
    response = client.post('/ratings/', data=json.dumps(rating_payload))
    assert response.status_code == 400

def test_with_non_existing_movie():
    rating_payload = {
        'movie': 2,
        'value': 4,
    }
    response = client.post('/ratings/', data=json.dumps(rating_payload))
    assert response.status_code == 400

'''#############################
#####  GetMovieTestCase  #####
#################################'''
# delete all recored from table
def test_delete_records():
    asyncio.run(delete_records())

def test_with_no_ratings():
    global movie
    movie = client.post('/movies/', data=json.dumps(movie_payload)).json()
    response = client.get(f'/movies/{movie["id"]}/')
    assert response.status_code == 200
    expected_movie = {
        'id': movie["id"],
        'title': movie_payload['title'],
        'rating': None,
    }
    assert response.json() == expected_movie


def test_with_two_ratings():
    rating_payloads = [
        {'movie': movie['id'], 'value': 4},
        {'movie': movie['id'], 'value': 5},
    ]

    for payload in rating_payloads:
        client.post('/ratings/', data=json.dumps(payload))

    response = client.get(f'/movies/{movie["id"]}/')
    assert response.status_code == 200

    expected_rating = sum(obj['value'] for obj in rating_payloads) / len(rating_payloads)
    expected_movie = {
        'id': movie['id'],
        'title': movie_payload['title'],
        'rating': expected_rating,
    }
    assert response.json() == expected_movie

def test_with_ratings_to_different_movies():
    another_movie = client.post('movies/', data=json.dumps({'title': 'Another movie'})).json()

    rating_payloads = [
        {'movie': another_movie['id'], 'value': 2},
        {'movie': movie['id'], 'value': 1},
        {'movie': another_movie['id'], 'value': 5},
    ]

    for payload in rating_payloads:
        client.post('/ratings/', data=json.dumps(payload))

    response = client.get(f'/movies/{another_movie["id"]}/')
    assert response.status_code == 200

    sum_expected_ratings = sum(obj['value'] for obj in rating_payloads
                               if obj['movie'] == another_movie['id'])
    num_expected_ratings = len([obj['value'] for obj in rating_payloads
                                if obj['movie'] == another_movie['id']])
    expected_movie = {
        'id': another_movie['id'],
        'title': another_movie['title'],
        'rating': sum_expected_ratings / num_expected_ratings,
    }
    assert response.json() == expected_movie


def test_with_non_existing_movie():
    not_exitsing_id = 12
    response = client.get(f'/movies/{not_exitsing_id}/')
    assert response.status_code == 404
