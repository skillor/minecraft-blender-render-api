import uvicorn
from fastapi import FastAPI, UploadFile, File, Header, Form
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from blender_renderer.renderer import Renderer
from minecraf_blender_render import MinecraftBlenderRender


class BytesFileResponse(Response):
    def __init__(self, content=bytes(), content_disposition='inline', filename=None, *args, **kwargs):
        if filename is not None:
            content_disposition = content_disposition + '; filename="{}"'.format(filename)
        headers = {
            'Content-Disposition': content_disposition,
        }
        if hasattr(content, 'read') and callable(content.read):
            content = content.read()
        if 'headers' in kwargs:
            headers = {**headers, **kwargs['headers']}
        super().__init__(
            *args,
            content=content,
            headers=headers,
            **kwargs,
        )


class Server:
    async def authorize(self, api_key: str):
        if self.api_keys is None:
            return
        if api_key is None:
            raise Exception('Api Key not provided')
        if api_key not in self.api_keys:
            raise Exception('Api Key is incorrect')

    def __init__(self,
                 renderer: MinecraftBlenderRender = None,
                 debug=False,
                 api_keys='',
                 cors_origins='',
                 ):
        super().__init__()

        cors_origins = cors_origins.split(',')
        api_keys = api_keys.split(',')

        if api_keys is not None and len(api_keys) == 0:
            api_keys = None
        self.api_keys = api_keys

        self.renderer = renderer

        docs_url = None
        redoc_url = None
        openapi_url = None
        if debug:
            docs_url = '/docs'
            redoc_url = '/redoc'
            openapi_url = '/openapi.json'

        self.app = FastAPI(
            title='Minecraft Blender Render Api',
            debug=debug,
            default_response_class=Response,
            docs_url=docs_url,
            redoc_url=redoc_url,
            openapi_url=openapi_url,
        )

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=cors_origins,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @self.app.post(path='/render-skin-auto')
        async def render_skin_auto(
                api_key: str = Header(default=''),
                scene_file: UploadFile = File(),
                replace_skins_steve: str = Form(default=''),
                replace_skins_alex: str = Form(default=''),
        ):
            await self.authorize(api_key)
            img_bytes = self.renderer.render_skin_auto(
                scene_file.file.read(),
                replace_skins_steve,
                replace_skins_alex,
            )
            return BytesFileResponse(
                img_bytes,
                filename='render.png',
                media_type='image/png',
            )

    def run(self):
        uvicorn.run(self.app)


def create_server(environment, settings=None, example_settings=None):
    if settings is None:
        settings = {}
    if example_settings is None:
        example_settings = {}

    def get_setting(key):
        v = environment.get(key)
        if v is not None:
            return v
        if key in settings:
            return settings[key]
        return example_settings[key]

    renderer = MinecraftBlenderRender(
        Renderer(get_setting('BLENDER_BIN_PATH'), get_setting('TMP_DIRECTORY'))
    )

    return Server(
        renderer=renderer,
        cors_origins=get_setting('CORS_ORIGINS'),
        api_keys=get_setting('API_KEYS'),
        debug=get_setting('WEBSERVER_DEBUG'),
    )
