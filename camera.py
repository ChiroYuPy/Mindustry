class Camera:
    def __init__(self, min_zoom=1, max_zoom=1, zoom_schedule=1.1):
        self.x = 0
        self.y = 0

        self.zoom = 1
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom
        self.zoom_schedule = zoom_schedule

    def world_to_screen(self, wx, wy, ox, oy, tile_size, with_zoom=False):
        zoom_factor = self.zoom if with_zoom else 1
        sx = (wx * tile_size - self.x) * zoom_factor + ox
        sy = (wy * tile_size - self.y) * zoom_factor + oy
        return sx, sy

    def screen_to_world(self, sx, sy, ox, oy, tile_size, with_zoom=False):
        zoom_factor = self.zoom if with_zoom else 1
        wx = ((sx - ox) / zoom_factor + self.x) // tile_size
        wy = ((sy - oy) / zoom_factor + self.y) // tile_size
        return wx, wy

    def zoom_in(self):
        self.zoom = max(self.zoom / self.zoom_schedule, self.min_zoom)

    def zoom_out(self):
        self.zoom = min(self.zoom * self.zoom_schedule, self.max_zoom)

    def move(self, dx, dy):
        self.x += dx / self.zoom
        self.y += dy / self.zoom
