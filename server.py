import base64
from typing import List

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

        @self.app.get(path='/authorize')
        async def status(
                api_key: str = Header(default=''),
        ):
            await self.authorize(api_key)
            return JSONResponse(content={'msg': 'success'})

        @self.app.post(path='/get-image-names')
        async def get_image_names(
                api_key: str = Header(default=''),
                scene_file: UploadFile = File(),
        ):
            await self.authorize(api_key)
            texture_names = self.renderer.blender_renderer.get_texture_names(scene_file.file.read())
            return JSONResponse(content={'msg': 'success', 'texture_names': texture_names})

        @self.app.post(path='/render')
        async def render(
                api_key: str = Header(default=''),
                scene_file: UploadFile = File(),
                texture_files: List[UploadFile] = None,
                render_settings: str = Form(default=None),
        ):
            await self.authorize(api_key)
            if texture_files is None:
                texture_files = []
            texture_files_map = {}
            for texture_file in texture_files:
                texture_files_map[texture_file.filename] = texture_file.file.read()
            img_bytes = self.renderer.blender_renderer.render(
                scene_file.file.read(),
                textures=texture_files_map,
                render_settings_string=render_settings,
            )
            return BytesFileResponse(
                img_bytes,
                filename='render.png',
                media_type='image/png',
            )

        @self.app.post(path='/unpack')
        async def unpack(
                api_key: str = Header(default=''),
                scene_file: UploadFile = File(),
        ):
            await self.authorize(api_key)
            textures = self.renderer.blender_renderer.unpack(scene_file.file.read())
            b64_textures = {}
            for texture_name in list(textures.keys()):
                b64_textures[texture_name] = base64.b64encode(textures[texture_name]).decode('utf8')
                del textures[texture_name]
            return JSONResponse(content={'msg': 'success', 'textures': b64_textures})

        @self.app.post(path='/get-render-settings')
        async def get_render_settings(
                api_key: str = Header(default=''),
                scene_file: UploadFile = File(),
        ):
            await self.authorize(api_key)
            render_settings = self.renderer.blender_renderer.get_render_settings(scene_file.file.read())
            return JSONResponse(content=render_settings)

        @self.app.post(path='/render-skin-auto')
        async def render_skin_auto(
                api_key: str = Header(default=''),
                scene_file: UploadFile = File(),
                replace_skins_steve: str = Form(default=''),
                replace_skins_alex: str = Form(default=''),
                replace_texture_files: List[UploadFile] = None,
                render_settings: str = Form(default=None),
        ):
            await self.authorize(api_key)

            if replace_texture_files is None:
                replace_texture_files = []
            replace_texture_file_map = {}
            for texture_file in replace_texture_files:
                replace_texture_file_map[texture_file.filename] = texture_file.file.read()

            img_bytes = self.renderer.render_skin_auto(
                scene_file.file.read(),
                replace_skins_steve,
                replace_skins_alex,
                replace_texture_file_map,
                render_settings,
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
