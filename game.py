import pygame

from camera import Camera
from config import *
from gui import GUI
from map_renderer import MapRenderer
from sprite_manager import SpriteManager
from tile import Tile, Conveyer, Starter
from tile_map import TileMap


class Editor:
    def __init__(self):
        self.selected_tile_type = "Tile"


class Game:
    def __init__(self):
        self.display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA)
        pygame.display.set_caption("Factorio de Wish")

        self.tile_map = TileMap()
        self.tile_map.load("save.json")
        self.items = []

        self.sprite_manager = SpriteManager()
        self.sprite_manager.load_sprite_sheet("assets/blocks/distribution/conveyors", "conveyor", 5, 4, 2)

        self.camera = Camera(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2)

        self.map_renderer = MapRenderer((DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2))

        self.editor = Editor()
        self.gui = GUI(self.editor)

        self.mouse_button_left_pressed = False
        self.running = True
        self.selected_tile_type = "Tile"  # Default type

    def add_item(self, item):
        self.items.append(item)

    def generate_tile(self, x, y, tile_type=0):
        self.tile_map[(x, y)] = Tile(tile_type)

    def generate_conveyer(self, x, y, direction):
        self.tile_map[(x, y)] = Conveyer(direction)

    def generate_starter(self, x, y, direction):
        self.tile_map[(x, y)] = Starter(direction)

    def draw(self):
        self.map_renderer.render(self.display, self.tile_map, self.camera)
        self.gui.draw(self.display)
        self.render_items()

    def render_items(self):
        for item in self.items:
            x, y = self.camera.world_to_screen(item.x*TILE_SIZE, item.y*TILE_SIZE)
            pygame.draw.circle(self.display, (255, 255, 0), (x, y), TILE_SIZE/4*self.camera.zoom)

    def update(self):
        self.sprite_manager.update_animation_frame()
        for (x, y), tile in self.tile_map.items():
            if isinstance(tile, Starter):
                tile.update(self, x, y)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.tile_map.save("save.json")
                elif event.key == pygame.K_l:
                    self.tile_map.load("save.json")
                elif event.key == pygame.K_c:
                    self.tile_map.clear()
                elif event.key == pygame.K_1:
                    self.selected_tile_type = "Tile"
                    self.editor.selected_tile_type = self.selected_tile_type
                elif event.key == pygame.K_2:
                    self.selected_tile_type = "Conveyer"
                    self.editor.selected_tile_type = self.selected_tile_type
                elif event.key == pygame.K_3:
                    self.selected_tile_type = "Starter"
                    self.editor.selected_tile_type = self.selected_tile_type
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_button_left_pressed = True
                elif event.button == 3:
                    x, y = event.pos
                    x, y = self.camera.screen_to_world(x, y)
                    x, y = x // TILE_SIZE, y // TILE_SIZE

                    if self.selected_tile_type == "Tile":
                        self.generate_tile(x, y)
                    elif self.selected_tile_type == "Conveyer":
                        self.generate_conveyer(x, y, 0)
                    elif self.selected_tile_type == "Starter":
                        self.generate_starter(x, y, 0)

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.mouse_button_left_pressed = False
            elif event.type == pygame.MOUSEMOTION and self.mouse_button_left_pressed:
                self.camera.x -= event.rel[0] / self.camera.zoom
                self.camera.y -= event.rel[1] / self.camera.zoom
            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    self.camera.zoom_in()
                elif event.y < 0:
                    self.camera.zoom_out()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.display.fill((24, 24, 24))
            self.draw()
            pygame.display.update()