from color import get_color
import pygame

from config import TILE_SIZE


class MapRenderer:
    def __init__(self, origin_pos, tile_size=TILE_SIZE):
        self.origin = origin_pos
        self.tile_size = tile_size

    def render(self, display, tile_map, camera):
        rect = pygame.Rect(0, 0, self.tile_size, self.tile_size)
        for pos, tile in tile_map.items():
            if tile:
                x, y = pos
                screen_pos = camera.world_to_screen((x-0.5) * self.tile_size, (y-0.5) * self.tile_size)
                rect.x = screen_pos[0]
                rect.y = screen_pos[1]
                rect.w = rect.h = self.tile_size * camera.zoom
                color = get_color(tile)
                pygame.draw.rect(display, color, rect)