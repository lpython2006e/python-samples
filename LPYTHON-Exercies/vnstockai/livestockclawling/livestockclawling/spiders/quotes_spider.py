import requests
import json

# API url
url = "https://footballapi.pulselive.com/football/players"

# Headers required for making a GET request
# It is a good practice to provide headers with each request.
headers = {
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "DNT": "1",
    "Origin": "https://www.premierleague.com",
    "Referer": "https://www.premierleague.com/players",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
}

# Query parameters required to make get request
queryParams = {
    "pageSize": 32,
    "compSeasons": 274,
    "altIds": True,
    "page": 0,
    "type": "player",
    "id": -1,
    "compSeasonId": 274
}

# Sending the request with url, headers, and query params
response = requests.get(url = url, headers = headers, params = queryParams)

# if response status code is 200 OK, then
if response.status_code == 200:
    # load the json data
    data = json.loads(response.text)
    # print the required data
    for player in data["content"]:
        print({
            "name": player["name"]["display"],
            "nationalTeam": player["nationalTeam"]["country"],
            "position": player["info"]["positionInfo"]
        })
