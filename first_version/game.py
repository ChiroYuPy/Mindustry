import time
import pygame
from camera import Camera
from config import *
from gui import GUI
from item import Item
from map_renderer import MapRenderer
from sprite_manager import SpriteManager
from tile import Tile, Conveyer, Starter, DirectionalTile, BasicConveyer, ArmoredConveyer, TitaniumConveyer, UpdatedTile
from tile_map import TileMap

class Editor:
    def __init__(self):
        self.tile_panel = [BasicConveyer, ArmoredConveyer, TitaniumConveyer]

        self.selected_tile_index = 0
        self.selected_tile_pos = (0, 0)
        self.selected_tile = None

    def next_tile(self):
        self.selected_tile_index = (self.selected_tile_index + 1) % len(self.tile_panel)

    @property
    def selected_tile_type(self):
        return self.tile_panel[self.selected_tile_index]

    @property
    def selected_tile_name(self):
        return self.selected_tile_type.__name__

    def handle_keydown(self, event, tile_map):
        if event.key == pygame.K_s:
            tile_map.save("save.json")
        elif event.key == pygame.K_l:
            tile_map.load("save.json")
        elif event.key == pygame.K_c:
            tile_map.clear()
        elif event.key == pygame.K_a:
            self.next_tile()
        elif event.key == pygame.K_e:
            if isinstance(self.selected_tile, Tile):
                self.selected_tile.variant = (self.selected_tile.variant + 1) % self.selected_tile.MAX_VARIANT
        elif event.key == pygame.K_r:
            if isinstance(self.selected_tile, DirectionalTile):
                self.selected_tile.direction = (self.selected_tile.direction + 1) % self.selected_tile.MAX_DIRECTION

class Game:
    def __init__(self):
        self.current_time = time.time()
        self.display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA)
        pygame.display.set_caption("Factorio de Wish")

        self.tile_map = TileMap()
        self.items = []

        self.sprite_manager = SpriteManager()
        self.sprite_manager.load_sprite_sheet("assets/blocks/distribution/conveyors", "conveyor", 5, 4, 8)
        self.sprite_manager.load_sprite_sheet("assets/blocks/distribution/conveyors", "armored-conveyor", 5, 4, 12)
        self.sprite_manager.load_sprite_sheet("assets/blocks/distribution/conveyors", "titanium-conveyor", 5, 4, 12)

        self.camera = Camera(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2)

        self.map_renderer = MapRenderer((DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2), self.sprite_manager)

        self.editor = Editor()
        self.gui = GUI(self.editor)

        self.mouse_button_left_pressed = False
        self.running = True

        for x in range(0, 16):
            self.generate_tile(x, 0)

        item = Item(0, 0)
        self.tile_map[(0, 0)].item = item
        self.add_item(item)

        item = Item(4, 0)
        self.tile_map[(4, 0)].item = item
        self.add_item(item)

    def add_item(self, item):
        self.items.append(item)

    def generate_tile(self, x, y):
        self.tile_map[(x, y)] = self.editor.selected_tile_type()

    def draw(self):
        self.map_renderer.render(self.display, self.tile_map, self.camera)
        self.render_items()
        self.draw_selection_cell()
        self.gui.draw(self.display)

    def render_items(self):
        for item in self.items:
            x, y = self.camera.world_to_screen(item.x + 0.5, item.y + 0.5)
            pygame.draw.circle(self.display, (255, 255, 0), (x, y), TILE_SIZE / 4 * self.camera.zoom)

    def draw_selection_cell(self):
        size = TILE_SIZE * self.camera.zoom
        x, y = self.editor.selected_tile_pos
        x, y = self.camera.world_to_screen(x, y)
        pygame.draw.rect(self.display, (255, 255, 255), (x, y, size, size), width=2)

    def update(self, dt):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x, y = self.camera.screen_to_world(mouse_x + 0.5, mouse_y + 0.5)
        self.editor.selected_tile_pos = (x, y)
        self.editor.selected_tile = self.tile_map[(x, y)]
        self.sprite_manager.update_animation_frame(self.camera.zoom)
        for (x, y), tile in self.tile_map.items():
            if isinstance(tile, UpdatedTile):
                tile.update(self, x, y, dt)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                self.editor.handle_keydown(event, self.tile_map)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_button_left_pressed = True
                elif event.button == 3:
                    x, y = event.pos
                    x, y = self.camera.screen_to_world(x, y)

                    self.generate_tile(x, y)

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
            last_time = self.current_time
            self.current_time = time.time()
            dt = self.current_time - last_time
            self.update(dt)
            self.display.fill((24, 24, 24))
            self.draw()
            pygame.display.update()
