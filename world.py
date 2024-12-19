import pygame


class World:
    def __init__(self, tile_map, texture_manager, tile_size):
        self.tile_map = tile_map
        self.texture_manager = texture_manager
        self.tile_size = tile_size

    def draw(self, display, camera, tick):
        for (x, y), tile in self.tile_map.tiles.items():
            self.draw_tile(display, camera, x, y, tile, frame=tick)

    def draw_tile(self, display, camera, x, y, tile, frame=0, alpha=255):
        texture = self.texture_manager.get_image(tile.tile_type, frame=frame)
        texture.convert_alpha()
        texture.set_alpha(alpha)

        window_width, window_height = display.get_size()
        tile_screen_x, tile_screen_y = camera.world_to_screen(x, y, window_width / 2, window_height / 2, self.tile_size)
        display.blit(texture, (tile_screen_x, tile_screen_y))

    def draw_tile_frame(self, display, camera, x, y, color=(127, 196, 255)):
        window_width, window_height = display.get_size()
        tile_screen_x, tile_screen_y = camera.world_to_screen(x, y, window_width / 2, window_height / 2, self.tile_size)
        pygame.draw.rect(display, color, (tile_screen_x, tile_screen_y, self.tile_size, self.tile_size),
                         width=int(self.tile_size / 16))

    def draw_tile_area_frame(self, display, camera, start_x, start_y, end_x, end_y, color=(127, 196, 255)):
        window_width, window_height = display.get_size()

        if start_x > end_x:
            temp = start_x
            start_x = end_x
            end_x = temp

        if start_y > end_y:
            temp = start_y
            start_y = end_y
            end_y = temp

        end_x += 1
        end_y += 1

        start_tile_screen_x, start_tile_screen_y = camera.world_to_screen(start_x, start_y, window_width / 2, window_height / 2, self.tile_size)
        end_tile_screen_x, end_tile_screen_y = camera.world_to_screen(end_x, end_y, window_width / 2, window_height / 2, self.tile_size)

        rect = (start_tile_screen_x, start_tile_screen_y, end_tile_screen_x - start_tile_screen_x, end_tile_screen_y - start_tile_screen_y)
        pygame.draw.rect(display, color, rect, width=int(self.tile_size / 16))
