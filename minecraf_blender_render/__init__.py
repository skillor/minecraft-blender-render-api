from typing import TYPE_CHECKING
import json

from minecraft_skin_converter import SkinConverter
from .skin import get_skin_bytes

if TYPE_CHECKING:
    from blender_renderer.renderer import Renderer as BlenderRenderer


class MinecraftBlenderRender:
    def __init__(self, blender_renderer: 'BlenderRenderer'):
        self.blender_renderer = blender_renderer

    def render_skin_auto(self,
                         scene_file_bytes: bytes,
                         replace_skins_steve: str,
                         replace_skins_alex: str,
                         ) -> bytes:

        texture_files_map = {}

        if replace_skins_steve != '':
            replace_skins_steve_dict = json.loads(replace_skins_steve)

            if not isinstance(replace_skins_steve_dict, dict):
                raise Exception('replace_skins_steve is not a dict')

            for texture_name, player_name in replace_skins_steve_dict.items():
                try:
                    skin_bytes = get_skin_bytes(player_name)
                    sc = SkinConverter()
                    sc.load_from_bytes(skin_bytes)
                    sc.normalize_skin()
                    if sc.is_valid_skin():
                        if not sc.is_steve():
                            sc.alex_to_steve()
                            skin_bytes = sc.save_to_bytes()
                        texture_files_map[texture_name] = skin_bytes
                except NameError:
                    pass

        if replace_skins_alex != '':
            replace_skins_alex_dict = json.loads(replace_skins_alex)

            if not isinstance(replace_skins_alex_dict, dict):
                raise Exception('replace_skins_alex is not a dict')

            for texture_name, player_name in replace_skins_alex_dict.items():
                try:
                    skin_bytes = get_skin_bytes(player_name)
                    sc = SkinConverter()
                    sc.load_from_bytes(skin_bytes)
                    sc.normalize_skin()
                    print(player_name, sc.is_valid_skin())
                    if sc.is_valid_skin():
                        if sc.is_steve():
                            sc.steve_to_alex()
                            skin_bytes = sc.save_to_bytes()
                        texture_files_map[texture_name] = skin_bytes
                except NameError:
                    pass

        img_bytes = self.blender_renderer.render(
            scene_file_bytes,
            textures=texture_files_map,
        )
        return img_bytes
