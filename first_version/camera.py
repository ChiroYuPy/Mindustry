from pygame.examples.grid import WINDOW_WIDTH, WINDOW_HEIGHT

from config import TILE_SIZE


class Camera:
    def __init__(self, origin_x, origin_y):
        self.x = 0
        self.y = 0
        self.ox = origin_x
        self.oy = origin_y
        self.zoom = 1
        self.max_zoom = 4
        self.min_zoom = 1
        self.zoom_schedule = 1.1

    def world_to_screen(self, wx, wy):
        sx = (wx * TILE_SIZE - self.x) * self.zoom + self.ox
        sy = (wy * TILE_SIZE - self.y) * self.zoom + self.oy
        return sx, sy

    def screen_to_world(self, sx, sy):
        wx = ((sx - self.ox) / self.zoom + self.x) // TILE_SIZE
        wy = ((sy - self.oy) / self.zoom + self.y) // TILE_SIZE
        return wx, wy

    def zoom_in(self):
        self.zoom = min(self.zoom * self.zoom_schedule, self.max_zoom)

    def zoom_out(self):
        self.zoom = max(self.zoom / self.zoom_schedule, self.min_zoom)

    def get_bounds(self):
        right = WINDOW_WIDTH / 2 * self.zoom
        left = right - WINDOW_WIDTH * self.zoom
        down = WINDOW_HEIGHT / 2 * self.zoom
        up = down - WINDOW_HEIGHT * self.zoom
        return left, right, up, down
