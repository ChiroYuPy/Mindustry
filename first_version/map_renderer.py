from config import TILE_SIZE
from tile import Conveyer


class MapRenderer:
    def __init__(self, origin_pos, sprite_manager, tile_size=TILE_SIZE):
        self.origin = origin_pos
        self.sprite_manager = sprite_manager
        self.tile_size = tile_size

    def render(self, display, tile_map, camera):
        for (x, y), tile in tile_map.items():
            if tile:
                x, y = camera.world_to_screen(x, y)
                if isinstance(tile, Conveyer):
                    image = tile.get_image(self.sprite_manager)
                    display.blit(image, (x, y, self.tile_size, self.tile_size))
