import os

current_dir = os.path.dirname(os.path.realpath(__file__))

GLOBAL_SETTINGS = {
    'WEBSERVER_DEBUG': False,
    'BLENDER_BIN_PATH': 'blender',
    'TMP_DIRECTORY': os.path.join(current_dir, 'tmp'),
    # CORS ORIGINS, separate by comma
    'CORS_ORIGINS': '*',
    # API KEYS, separate by comma
    'API_KEYS': '',
}
