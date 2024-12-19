import pygame


class World:
    def __init__(self, tile_map, texture_manager, tile_size):
        self.tile_map = tile_map
        self.texture_manager = texture_manager
        self.tile_size = tile_size

    def draw(self, display, camera, tick):
        for (x, y), tile in self.tile_map.tiles.items():
            window_width, window_height = display.get_size()
            tile_screen_x, tile_screen_y = camera.world_to_screen(x, y, window_width / 2, window_height / 2, self.tile_size)

            if not ( -self.tile_size < tile_screen_x < window_width and -self.tile_size < tile_screen_y < window_height):
                continue # basic culling

            texture = self.texture_manager.get_image(tile.tile_type, frame=tick)
            display.blit(texture, (tile_screen_x, tile_screen_y))

    def draw_tile(self, display, camera, x, y, tile, frame=0, alpha=255):
        window_width, window_height = display.get_size()
        tile_screen_x, tile_screen_y = camera.world_to_screen(x, y, window_width / 2, window_height / 2, self.tile_size)

        texture = self.texture_manager.get_image(tile.tile_type, frame=frame)
        texture.convert_alpha()
        texture.set_alpha(alpha)
        display.blit(texture, (tile_screen_x, tile_screen_y))

    def draw_tile_frame(self, display, camera, x, y, color=(127, 196, 255)):
        window_width, window_height = display.get_size()
        tile_screen_x, tile_screen_y = camera.world_to_screen(x, y, window_width / 2, window_height / 2, self.tile_size)
        pygame.draw.rect(display, color, (tile_screen_x, tile_screen_y, self.tile_size, self.tile_size),
                         width=int(self.tile_size / 16))

    def draw_tile_area_frame(self, display, camera, start_x, start_y, end_x, end_y, color=(127, 196, 255)):
        window_width, window_height = display.get_size()

        # adjust start and end position to allways have a rect that start at up left corner and end at down right corner
        if start_x > end_x:
            temp = start_x
            start_x = end_x
            end_x = temp

        if start_y > end_y:
            temp = start_y
            start_y = end_y
            end_y = temp

        # adjust area to draw the bound hover all the tiles
        end_x += 1
        end_y += 1

        start_tile_screen_x, start_tile_screen_y = camera.world_to_screen(start_x, start_y, window_width / 2, window_height / 2, self.tile_size)
        end_tile_screen_x, end_tile_screen_y = camera.world_to_screen(end_x, end_y, window_width / 2, window_height / 2, self.tile_size)

        bound = (start_tile_screen_x, start_tile_screen_y, end_tile_screen_x - start_tile_screen_x, end_tile_screen_y - start_tile_screen_y)
        pygame.draw.rect(display, color, bound, width=int(self.tile_size / 16))
