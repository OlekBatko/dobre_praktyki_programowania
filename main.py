from fastapi import FastAPI, Query
from fastapi.responses import Response
import csv
import json
from typing import List, Dict

app = FastAPI()


class Movie:
    def __init__(self, movie_id: str, title: str, genres: str):
        self.id = str(movie_id)
        self.title = title
        self.genres = genres

class Link:
    def __init__(self, movie_id: str, imdb_id: str, tmdb_id: str):
        self.movieId = str(movie_id)
        self.imdbId = str(imdb_id) if imdb_id is not None else ""
        self.tmdbId = str(tmdb_id) if tmdb_id is not None else ""

class Rating:
    def __init__(self, user_id: str, movie_id: str, rating: float, timestamp: int):
        self.userId = str(user_id)
        self.movieId = str(movie_id)
        self.rating = float(rating)
        self.timestamp = int(timestamp)

class Tag:
    def __init__(self, user_id: str, movie_id: str, tag: str, timestamp: int):
        self.userId = str(user_id)
        self.movieId = str(movie_id)
        self.tag = tag
        self.timestamp = int(timestamp)


def pretty_json(data: List[Dict]) -> Response:
    return Response(
        content=json.dumps(data, ensure_ascii=False, indent=4),
        media_type="application/json"
    )

def read_csv(path: str) -> List[Dict[str, str]]:
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


@app.get("/hello")
def hello_world():
    return {"hello": "world"}

@app.get("/movies")
def get_movies(
    limit: int = Query(100, ge=1, le=10000),
    offset: int = Query(0, ge=0),
):
    rows = read_csv("database/movies.csv")[offset: offset + limit]
    movies = [
        Movie(
            movie_id=r.get("movieId", r.get("id", "")),
            title=r.get("title", ""),
            genres=r.get("genres", ""),
        ).__dict__
        for r in rows
    ]
    return pretty_json(movies)

@app.get("/links")
def get_links(
    limit: int = Query(100, ge=1, le=10000),
    offset: int = Query(0, ge=0),
):
    rows = read_csv("database/links.csv")[offset: offset + limit]
    links = [
        Link(
            movie_id=r.get("movieId", ""),
            imdb_id=r.get("imdbId", ""),
            tmdb_id=r.get("tmdbId", ""),
        ).__dict__
        for r in rows
    ]
    return pretty_json(links)

@app.get("/ratings")
def get_ratings(
    limit: int = Query(100, ge=1, le=10000),
    offset: int = Query(0, ge=0),
):
    rows = read_csv("database/ratings.csv")[offset: offset + limit]
    ratings = []
    for r in rows:
        try:
            ratings.append(
                Rating(
                    user_id=r.get("userId", ""),
                    movie_id=r.get("movieId", ""),
                    rating=float(r.get("rating", 0.0)),
                    timestamp=int(r.get("timestamp", 0)),
                ).__dict__
            )
        except ValueError:
            continue
    return pretty_json(ratings)

@app.get("/tags")
def get_tags(
    limit: int = Query(100, ge=1, le=10000),
    offset: int = Query(0, ge=0),
):
    rows = read_csv("database/tags.csv")[offset: offset + limit]
    tags = []
    for r in rows:
        try:
            tags.append(
                Tag(
                    user_id=r.get("userId", ""),
                    movie_id=r.get("movieId", ""),
                    tag=r.get("tag", ""),
                    timestamp=int(r.get("timestamp", 0)),
                ).__dict__
            )
        except ValueError:
            continue
    return pretty_json(tags)
