import pygame


class World:
    def __init__(self, tile_map, texture_manager, tile_size):
        self.tile_map = tile_map
        self.texture_manager = texture_manager
        self.tile_size = tile_size

    def draw(self, surface, camera, tick=0):
        window_width, window_height = surface.get_size()
        sub_surface_width, sub_surface_height = window_width / camera.zoom, window_height / camera.zoom
        sub_surface = pygame.Surface((window_width/camera.zoom, window_height/camera.zoom)).convert_alpha()
        for (x, y), tile in self.tile_map.tiles.items():
            texture = self.texture_manager.get_image(tile.tile_type, frame=tick)
            if texture:
                x, y = camera.world_to_screen(x, y, sub_surface_width/2, sub_surface_height/2, self.tile_size, with_zoom=False)
                sub_surface.blit(texture, (x, y))

        sub_surface_width, sub_surface_height = sub_surface.get_width()*camera.zoom, sub_surface.get_height()*camera.zoom
        sub_surface = pygame.transform.scale(sub_surface, (sub_surface_width, sub_surface_height))
        surface.blit(sub_surface, (window_width/2-sub_surface_width/2, window_height/2-sub_surface_height/2))

    def draw_preview_tile(self, surface, camera, x, y, tile):
        texture = self.texture_manager.get_image(tile.tile_type, frame=0)

        window_width, window_height = surface.get_size()

        tile_screen_x, tile_screen_y = camera.world_to_screen(x, y, window_width // 2, window_height // 2, self.tile_size, with_zoom=True)

        scaled_texture = pygame.transform.scale(texture, (int(texture.get_width() * camera.zoom), int(texture.get_height() * camera.zoom))).convert_alpha()
        scaled_texture.set_alpha(64)

        surface.blit(scaled_texture, (tile_screen_x, tile_screen_y))