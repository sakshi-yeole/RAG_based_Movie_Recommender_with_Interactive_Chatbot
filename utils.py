import requests

TMDB_API_KEY = "TMDB_API_KEY"
TMDB_BASE_URL = "https://api.themoviedb.org/3"
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w342"

def get_tmdb_id(title):
    try:
        url = f"{TMDB_BASE_URL}/search/movie"
        response = requests.get(url, params={"api_key": TMDB_API_KEY, "query": title})

        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            if results:
                return results[0]["id"]
    except:
        pass

    return None


def get_movie_poster_by_title(title):
    tmdb_id = get_tmdb_id(title)
    if not tmdb_id:
        return None

    try:
        url = f"{TMDB_BASE_URL}/movie/{tmdb_id}?api_key={TMDB_API_KEY}"
        response = requests.get(url).json()

        poster_path = response.get("poster_path")
        if poster_path:
            return POSTER_BASE_URL + poster_path
    except:
        pass

    return None
