import string
import requests
import os
from dotenv import load_dotenv
import shutil

load_dotenv()

STEAM_ID = os.getenv("STEAM_ID")
STEAM_KEY = os.getenv("STEAM_KEY")
ICON_PATH = "game_icons"
URLS = {
    "OWNED_GAMES": "http://api.steampowered.com/IPlayerService/GetOwnedGames/v1",
    "GAME_ICON": "https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps",
    "GAME_DETAILS": "https://store.steampowered.com/api/appdetails",
}


def format_filename(s):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = "".join(c for c in s if c in valid_chars)
    filename = filename.replace(" ", "_")
    return filename


def get_library_games(steam_key: str, steam_id: str):
    steam_url = f"{URLS['OWNED_GAMES']}/?key={steam_key}&steamid={steam_id}&format=json&include_appinfo=true"
    response = requests.get(steam_url)

    if response.status_code == 200:
        games = response.json()["response"]["games"]
        return games
    else:
        print(f"Error getting games: {response.status_code}")
        return


def get_game_icon(folder_path, game):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    formated_name = format_filename(game["name"])

    icon_url = f"{URLS['GAME_ICON']}/{game['appid']}/{game['img_icon_url']}.jpg"
    response = requests.get(icon_url, stream=True)

    file_name = f"{folder_path}/{formated_name}.png"
    if response.status_code == 200:
        with open(file_name, "wb") as f:
            shutil.copyfileobj(response.raw, f)
        return file_name
    else:
        print(f"Error getting icons: {response.status_code}")
        return


def get_game_details(game):
    response = requests.get(f"{URLS['GAME_DETAILS']}?appids={game['appid']}&l=english")
    game_info = response.json()[{game["appid"]}]["data"]

    print(game_info)
    desc = game_info["detailed_description"]
    print(desc)
