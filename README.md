# Minecraft Blender Renderer Python

### Docs

API-Documentation can be found here: https://skillor.github.io/minecraft-blender-render-api/

## Installation

All settings can be overwritten with environment variables with the same name.

### Run as Docker container

> with port and API KEY

    docker run --rm -d -p 8000:80 --env API_KEYS=123qwe skillor/minecraft-blender-render-api

docker image can be found here: https://hub.docker.com/r/skillor/minecraft-blender-render-api

### Setup in Unix

> Install Blender

> Install API requirements

```bash
pip3 install -r requirements.txt
```

> Copy "settings_example.py" to "settings.py"

```bash
cp settings_example.py settings.py
```

> Edit your settings.py

> Start the server

```bash
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --log-level warning
```
