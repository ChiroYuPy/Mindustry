

class Camera:
    def __init__(self, origin_x, origin_y):
        self.x = 0
        self.y = 0
        self.ox = origin_x
        self.oy = origin_y
        self.zoom = 1.0
        self.max_zoom = 4.0
        self.min_zoom = 0.4
        self.zoom_schedule = 1.1

    def world_to_screen(self, wx, wy):
        sx = (wx - self.x) * self.zoom + self.ox
        sy = (wy - self.y) * self.zoom + self.oy
        return sx, sy

    def screen_to_world(self, sx, sy):
        wx = (sx - self.ox) / self.zoom + self.x
        wy = (sy - self.oy) / self.zoom + self.y
        return wx, wy

    def zoom_in(self):
        self.zoom = min(self.zoom * self.zoom_schedule, self.max_zoom)

    def zoom_out(self):
        self.zoom = max(self.zoom / self.zoom_schedule, self.min_zoom)