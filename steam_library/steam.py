import requests


URLS = {
    "OWNED_GAMES": "http://api.steampowered.com/IPlayerService/GetOwnedGames/v1",
    "GAME_ICON": "https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps",
    "GAME_DETAILS": "https://store.steampowered.com/api/appdetails",
}


def get_library_games(steam_key: str, steam_id: str):
    steam_url = f"{URLS['OWNED_GAMES']}/?key={steam_key}&steamid={steam_id}&format=json&include_appinfo=true"
    response = requests.get(steam_url)

    if response.status_code == 200:
        games = response.json()["response"]["games"]
        return games
    else:
        print(f"Error getting games: {response.status_code}")
        return


def get_game_details(game):
    response = requests.get(f"{URLS['GAME_DETAILS']}?appids={game['appid']}&l=english")
    if response.status_code == 200:
        if "data" in response.json()[str(game["appid"])]:
            game_info = response.json()[str(game["appid"])]["data"]
            return game_info
    else:
        print(f"Error getting game details: {response.status_code}")
        return
