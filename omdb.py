import requests

API_KEY = "84936fd0"

def get_movie_data(title):
    url = "https://www.omdbapi.com/"

    params = {
        "apikey": API_KEY,
        "t": title
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data.get("Response") == "True":
        return data

    # Try searching if exact title fails
    params = {
        "apikey": API_KEY,
        "s": title
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data.get("Response") == "True":
        movie = data["Search"][0]

        response = requests.get(
            url,
            params={
                "apikey": API_KEY,
                "i": movie["imdbID"]
            }
        )

        return response.json()

    return None