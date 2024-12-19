import pygame


class Camera:
    def __init__(self, min_zoom=1, max_zoom=1, zoom_schedule=1.1):
        self._position = pygame.Vector2(0, 0)

        self._zoom = 1
        self._min_zoom = min_zoom
        self._max_zoom = max_zoom
        self._zoom_schedule = zoom_schedule

    @property
    def x(self):
        return self._position.x

    @property
    def y(self):
        return self._position.y

    @property
    def zoom(self):
        return self._zoom

    def world_to_screen(self, wx, wy, ox, oy, tile_size, with_zoom=False):
        zoom_factor = self.zoom if with_zoom else 1
        sx = (wx * tile_size - self._position.x) * zoom_factor + ox
        sy = (wy * tile_size - self._position.y) * zoom_factor + oy
        return sx, sy

    def screen_to_world(self, sx, sy, ox, oy, tile_size, with_zoom=False):
        zoom_factor = self._zoom if with_zoom else 1
        wx = ((sx - ox) / zoom_factor + self._position.x) // tile_size
        wy = ((sy - oy) / zoom_factor + self._position.y) // tile_size
        return wx, wy

    def zoom_in(self):
        self._zoom = max(self._zoom / self._zoom_schedule, self._min_zoom)

    def zoom_out(self):
        self._zoom = min(self._zoom * self._zoom_schedule, self._max_zoom)

    def move(self, dx, dy):
        self._position.x += dx / self._zoom
        self._position.y += dy / self._zoom