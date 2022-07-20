import requests
import json
import re


def get_skin_bytes(player_name):
    match = re.match('([a-zA-Z0-9_]{3,16})', player_name)
    if match is None:
        raise NameError(f'invalid player name: {player_name}')
    player_name = match.group()
    response = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{player_name}')
    if response.status_code != 200:
        raise NameError(f'something went wrong while fetching skin for {player_name}')

    response_json = json.loads(response.content)

    uuid = response_json['id']
    return requests.get(f'https://crafatar.com/skins/{uuid}').content
