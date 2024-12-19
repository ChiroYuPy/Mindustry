import sys
import pygame

from camera import Camera
from clock import Clock
from editor import Editor
from image_manager import ImageManager
from item import Item
from loader import load_textures
from tile import Tile
from tile_entity import ConveyorTE
from tile_map import TileMap
from world import World


class Game:
    def __init__(self):
        self.display = pygame.display.set_mode((1920, 1080), pygame.SRCALPHA)
        self.clock = Clock()

        self.tile_size = 64

        self.camera = Camera()

        self.image_manager = ImageManager("assets/")
        load_textures(self.image_manager)
        self.image_manager.resize(self.tile_size)

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
            self.editor.draw(self.display)
            pygame.display.flip()

            delta_time = self.clock.update(1000)
            # print(1/delta_time)


if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()
