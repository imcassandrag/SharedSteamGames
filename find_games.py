#libraries
import requests
import time

#configuring
#api found on: https://steamcommunity.com/dev/apikey
api_num = "Add API Number Here"

#user ids found on: https://steamid.io/lookup
user_id = [
    "User Number",  # User
    "User Number",  # Friend 1
    "User Number"   # Friend 2
]

#showing number of owned games for each person
def owned_games(steam_id):
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
    params = {
        "key": api_num, 
        "steamid": steam_id,
        "include_appinfo": True, #needed to find co-op game descriptions
        "format": "json"
    }
    response = requests.get(url, params=params)
    games = response.json().get("response", {}).get("games", [])
    return {game["appid"]: game["name"] for game in games}

#
def is_coop_game(appid):
    store_url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=us"
    try:
        response = requests.get(store_url)
        data = response.json()
        game_data = data[str(appid)]['data']
        categories = game_data.get('categories', [])
        for cat in categories:
            if 'Co-op' in cat.get('description', ''):
                return True
            if 'Multiplayer' in cat.get('description', ''):
                return True
        return False
    except Exception:
        return False

#Main
game_dicts = []
for steam_id in user_id:
    print(f"Fetching games for: {steam_id}")
    game_dict = owned_games(steam_id)
    print(f" - Found {len(game_dict)} games.\n")
    game_dicts.append(game_dict)

#finding shared games by AppID
shared_appids = set(game_dicts[0].keys())
for other in game_dicts[1:]:
    shared_appids &= set(other.keys())

#printing total number of shared games before printing co-op status of each
print(f"Total Shared Co-op Games: {len(shared_appids)}")

#printing shared games and co-op results
coop_games = []
for appid in shared_appids:
    name = game_dicts[0][appid]
    if is_coop_game(appid):
        coop_games.append(name)
        print(f"✅ {name}")
    else:
        print(f"❌ {name} (not co-op)")
    time.sleep(0.2) #slight pause between requests
