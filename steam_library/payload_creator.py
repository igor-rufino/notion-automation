import calendar


URLS = {
    "OWNED_GAMES": "http://api.steampowered.com/IPlayerService/GetOwnedGames/v1",
    "GAME_ICON": "https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps",
    "GAME_DETAILS": "https://store.steampowered.com/api/appdetails",
}


def convert_to_hours_minutes(minutes):
    hours = minutes // 60
    remaining_minutes = minutes % 60
    return f"{hours}h {remaining_minutes:02d}m"


def convert_release_date(release_date):
    rds = release_date.split()
    if len(rds) == 3:
        month = rds[1][:-1]
        if month in list(calendar.month_abbr):
            s_mn = list(calendar.month_abbr).index(month)
            new_release_date = f"{int(rds[2]):04d}-{int(s_mn):02d}-{int(rds[0]):02d}"

    else:
        month = rds[0]
        if month in list(calendar.month_abbr):
            s_mn = list(calendar.month_abbr).index(month)
            new_release_date = f"{int(rds[1]):04d}-{int(s_mn):02d}-01"

    return new_release_date


def generate_genre_list(game_info):
    genre_list = []
    for genre in game_info["genres"]:
        genre_list.append({"name": genre["description"]})
    return genre_list


def create_properties(game, game_info):
    properties = {
        "Time Played": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": convert_to_hours_minutes(game["playtime_forever"])
                    },
                }
            ],
        },
        "Minutes": {"number": game["playtime_forever"]},
        "Store Page": {
            "url": f"https://store.steampowered.com/app/{game['appid']}/",
        },
        "Publishers": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {"content": game_info["publishers"][0]},
                }
            ],
        },
        "Metacritic": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": str(game_info["metacritic"]["score"])
                        if "metacritic" in game_info
                        else "-"
                    },
                }
            ],
        },
        "Release Date": {
            "date": {"start": convert_release_date(game_info["release_date"]["date"])},
        },
        "Game ID": {
            "rich_text": [
                {"type": "text", "text": {"content": str(game_info["steam_appid"])}}
            ],
        },
        "Developers": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {"content": game_info["developers"][0]},
                }
            ],
        },
        "Genres": {"multi_select": generate_genre_list(game_info)},
        "Name": {
            "title": [
                {
                    "type": "text",
                    "text": {"content": game_info["name"]},
                }
            ],
        },
    }

    return properties


def create_children(game_info):
    children = [
        {
            "object": "block",
            "heading_2": {"rich_text": [{"text": {"content": "Description"}}]},
        },
        {
            "object": "block",
            "paragraph": {
                "rich_text": [
                    {
                        "text": {
                            "content": game_info["short_description"],
                        }
                    }
                ],
                "color": "default",
            },
        },
    ]
    return children


def create_icon(game):
    icon = {
        "type": "external",
        "external": {
            "url": f"{URLS['GAME_ICON']}/{game['appid']}/{game['img_icon_url']}.jpg"
        },
    }
    return icon


def create_cover(game_info):
    cover = {
        "type": "external",
        "external": {"url": game_info["header_image"].split("?")[0]},
    }
    return cover


def payload(steamdb_id, game, game_info):
    icon = create_icon(game)
    cover = create_cover(game_info)
    properties = create_properties(game, game_info)
    children = create_children(game_info)

    p = {
        "parent": {"database_id": steamdb_id},
        "cover": cover,
        "icon": icon,
        "properties": properties,
        "children": children,
    }
    return p
