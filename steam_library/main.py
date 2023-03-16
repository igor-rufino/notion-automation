import requests
import os
from dotenv import load_dotenv
import steam
import payload_creator


load_dotenv()

NOTION_KEY = os.getenv("NOTION_KEY")
NOTION_STEAMDB_ID = os.getenv("NOTION_STEAMDB_ID")
STEAM_ID = os.getenv("STEAM_ID")
STEAM_KEY = os.getenv("STEAM_KEY")

URLS = {"NOTION": "https://api.notion.com/v1"}


def get_database_items():
    url = f"{URLS['NOTION']}/databases/{NOTION_STEAMDB_ID}/query"
    payload = {"page_size": 1000}
    headers = {
        "Authorization": "Bearer " + NOTION_KEY,
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "content-type": "application/json",
    }
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response
    else:
        print(f"Error getting database items: {response.status_code}")
        return


def create_page(game, game_info):
    import requests

    url = f"{URLS['NOTION']}/pages"

    headers = {
        "Authorization": "Bearer " + NOTION_KEY,
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "content-type": "application/json",
    }

    response = requests.post(
        url,
        json=payload_creator.payload(NOTION_STEAMDB_ID, game, game_info),
        headers=headers,
    )
    if response.status_code != 200:
        print(f"Error creating page: {response.status_code}")
    return response


def run():
    games = steam.get_library_games(steam_key=STEAM_KEY, steam_id=STEAM_ID)

    created_pages = 0
    for game in games:
        game_info = steam.get_game_details(game)
        if game_info:
            response = create_page(game, game_info)
            if response.status_code == 200:
                created_pages += 1
    print(f"Successfully created {created_pages} new pages")


if __name__ == "__main__":
    run()
