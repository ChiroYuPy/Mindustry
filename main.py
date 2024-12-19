import sys
import time
import pygame

from camera import Camera
from image_manager import ImageManager
from item import Item
from loader import load_textures
from tile import Tile
from tile_entity import ConveyorTE
from tile_map import TileMap
from world import World


class Clock:
    def __init__(self):
        self.tick = 0
        self.total_time = 0
        self.current_time = time.time()

    def update(self, fps):
        last_time = self.current_time
        self.current_time = time.time()
        delta_time = self.current_time - last_time
        self.total_time += delta_time
        self.tick = int(self.total_time * 60)

        time.sleep(1/(fps*1.1))

        return delta_time


class Editor:
    def __init__(self, game):
        self.display = game.display
        self.world = game.world
        self.camera = game.camera
        self.tile_map = game.tile_map
        self.tile_size = game.tile_size

        self.selected_tile_pos = None
        self.preview_tile_pos = None

        self.preview_tile = Tile(tile_entity=ConveyorTE(), tile_type="conveyor-basic-normal")

        self.mouse_button_right = False

        self.mouse_pos = (0, 0)

    def draw(self):
        self.draw_cursor()

    def draw_cursor(self):
        x, y = self.preview_tile_pos
        if self.tile_map.get_tile(x, y):
            size = self.tile_size * self.camera.zoom
            x, y = self.preview_tile_pos
            x, y = self.camera.world_to_screen(x, y, self.display.get_width() // 2, self.display.get_height() / 2,
                                               self.tile_size, with_zoom=True)

            pygame.draw.rect(self.display, (127, 196, 255), (x, y, size, size), width=int(2 * self.camera.zoom))
        else:
            x, y = self.preview_tile_pos
            self.world.draw_preview_tile(self.display, self.camera, x, y, self.preview_tile)

    def update_preview_pos(self):
        x, y = self.mouse_pos
        world_pos = self.camera.screen_to_world(x, y, self.display.get_width()//2, self.display.get_height()/2, self.tile_size, with_zoom=True)
        x, y = world_pos
        self.preview_tile_pos = x, y

    def select_tile(self):
        x, y = self.mouse_pos
        world_pos = self.camera.screen_to_world(x, y, self.display.get_width()//2, self.display.get_height()/2, self.tile_size, with_zoom=True)
        x, y = world_pos
        self.selected_tile_pos = x, y

    def place_tile(self):
        if self.selected_tile_pos:
            x, y = self.selected_tile_pos
            self.tile_map.place_tile(x, y, Tile(tile_entity=ConveyorTE(), tile_type="conveyor-basic-normal"))

    def rotate_preview_tile(self):
        self.preview_tile.rotation = (self.preview_tile.rotation + 1) % 4

    def handle_events(self, event):
        self.mouse_pos = pygame.mouse.get_pos()
        self.update_preview_pos()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.place_tile()
            elif event.key == pygame.K_r:
                self.rotate_preview_tile()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                self.mouse_button_right = True
            elif event.button == 1:
                self.select_tile()
        elif event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                self.camera.zoom_out()
            elif event.y < 0:
                self.camera.zoom_in()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                self.mouse_button_right = False
        elif event.type == pygame.MOUSEMOTION:
            if self.mouse_button_right:
                dx, dy = event.rel
                self.camera.move(-dx, -dy)



class Game:
    def __init__(self):
        self.display = pygame.display.set_mode((800, 800))
        self.clock = Clock()

        self.tile_size = 32

        self.camera = Camera()

        self.image_manager = ImageManager("../assets/")
        load_textures(self.image_manager)

        self.tile_map = TileMap()
        self.tile_map.place_tile(0, 0, Tile("sol"))
        self.tile_map.place_tile(1, 0, Tile("conveyor-basic-normal", tile_entity=ConveyorTE(0).items.append(Item(0))))
        self.tile_map.place_tile(0, 1, Tile("conveyor-titanium-corner", tile_entity=ConveyorTE(0)))

        self.world = World(self.tile_map, self.image_manager, self.tile_size)

        self.editor = Editor(self)

        self.mouse_button_left = False

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.editor.handle_events(event)

            self.tile_map.update()

            self.display.fill((24, 24, 24))
            self.world.draw(self.display, self.camera, tick=self.clock.tick)
            self.editor.draw()
            pygame.display.flip()

            delta_time = self.clock.update(60)
            print(1/delta_time)


if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()