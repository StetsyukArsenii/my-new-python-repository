from urllib.parse import quote
from pprint import pprint

import os
import requests
import pandas as pd
from dotenv import load_dotenv
from wordcloud import WordCloud, STOPWORDS


load_dotenv()
TMDB_API_KEY = os.environ.get("TMDB_API_KEY")


def search_film_info(search_query: str) -> pd.DataFrame:
    imdb_films = search_imdb(search_query)
    films_list = []
    for film in imdb_films:
        img = film.get("i")
        img_url = None
        if img:
            img_url = img.get("imageUrl")
        id_   = film.get("id")
        title = film.get("l")
        rank  = film.get("rank")
        year  = film.get("y")

        cinemeta = search_cinemeta(id_)
        rating   = None
        duration = None
        if cinemeta:
            rating   = cinemeta.get("imdbRating")
            duration = cinemeta.get("runtime") # TODO: maybe need float in the future
            if rating:
                rating = float(rating)

        reviews = search_themoviedb(id_)

        films_list.append(
            {
                 "id"       : id_,
                 "title"    : title,
                 "year"     : year,
                 "duration" : duration,
                 "rank"     : rank,
                 "rating"   : rating,
                 "reviews"  : reviews,
                 "img_url"  : img_url
             }
        )

    return pd.DataFrame(films_list)

def search_imdb(search_query: str) -> list|None:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    search_query = quote(search_query.strip())
    search_url = f"https://v3.sg.media-imdb.com/suggestion/x/{search_query}.json"
    response = requests.get(search_url, headers=headers)

    rjson = response.json()
    films = rjson["d"]

    return films

def search_cinemeta(film_id: str) -> dict|None:
    for kind in ["movie", "series"]:
        url = f"https://v3-cinemeta.strem.io/meta/{kind}/{film_id}.json"
        try:
            response = requests.get(url).json()
            return response.get("meta")
        except requests.exceptions.JSONDecodeError:
            return None


def search_themoviedb(film_id: str) -> list[str]|None:
    base_url = f"https://api.themoviedb.org/3"
    url_find = f"{base_url}/find/{film_id}"
    query = {"api_key": TMDB_API_KEY, "external_source": "imdb_id", "language": "en-US"}
    try:
        response = requests.get(url_find, params=query, timeout=20).json()
    except requests.exceptions.JSONDecodeError as e:
        print(f"ERROR: {e}")
        return None

    media_type = None
    tmdb_id = None
    for key in response.keys():
        if not response[key]:
            continue
        movie_info = response[key]
        media_type = movie_info[0].get("media_type")
        tmdb_id = movie_info[0].get("id")
    
    if media_type is None or tmdb_id is None:
        print("ERROR: Failed to get 'tmdb_id' or 'media_type'")
        return None

    url_review = f"{base_url}/{media_type}/{tmdb_id}/reviews"
    query = {"api_key": TMDB_API_KEY, "language": "en-US"}
    try:
        response = requests.get(url_review, params=query, timeout=20).json()
    except requests.exceptions.JSONDecodeError as e:
        print(f"ERROR: {e}")
        return None

    reviews = []
    results = response.get("results")
    if not results:
        return None

    for review in results:
        content = review.get("content")
        reviews.append(content)

    return reviews



def reviews_to_wordcloud(reviews: list[dict], file_name: str) -> None: 
    text = " ".join(reviews)
    stopwords = list(STOPWORDS.copy()) + ["film", "MOVIE", "series", "movie", "film's", "movie's", "series's", "one", "like", "good", "great", "bad", "really", "just"]
    wc = WordCloud(width = 800, height = 400, background_color = 'white', stopwords = stopwords).generate(text)
    wc.to_file(file_name)

if __name__ == "__main__":
    df = search_film_info("Trap")
    df.to_html("file_info_table.html")
    reviews_to_wordcloud(df.iloc[0]["reviews"], "reviews_wordcloud.png")
