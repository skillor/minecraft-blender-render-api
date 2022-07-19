import requests
import json


def get_skin_bytes(player_name):
    response = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{player_name}')
    if response.status_code != 200:
        raise NameError(f'something went wrong while fetching skin for {player_name}')

    response_json = json.loads(response.content)

    uuid = response_json['id']
    return requests.get(f'https://crafatar.com/skins/{uuid}').content
