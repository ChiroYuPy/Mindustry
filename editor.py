import copy

import pygame

from tile import Tile
from tile_entity import ConveyorTE
from ui import Container, Button


class Editor:
    def __init__(self, game):
        self.display = game.display
        self.world = game.world
        self.camera = game.camera
        self.tile_map = game.tile_map
        self.tile_size = game.tile_size
        self.display_width = self.display.get_width()
        self.display_height = self.display.get_height()

        self.mouse_pos = (0, 0)

        self.start_selection_tile_pos = None
        self.end_selection_tile_pos = None

        self.selected_tile_pos = None
        self.preview_tile_pos = None

        self.selected_tile = None
        self.preview_tile = Tile(tile_entity=ConveyorTE(), tile_type="conveyor-basic-normal")

        self.mouse_button_right = False
        self.mouse_button_left = False

        self.tool = "selection"

        self.main_container = Container(0, self.display_height * 0.25, 128, self.display_height * 0.5,
                                        (32, 32, 32, 127))

        self.buttons = [
            Button(self.main_container.width / 2 - 32, 32, 64, 64, (48, 48, 48), (64, 64, 64), (96, 96, 96),
                   self.button_action_1),
            Button(self.main_container.width / 2 - 32, 128, 64, 64, (48, 48, 48), (64, 64, 64), (96, 96, 96),
                   self.button_action_2),
            Button(self.main_container.width / 2 - 32, 224, 64, 64, (48, 48, 48), (64, 64, 64), (96, 96, 96),
                   self.button_action_3),
            Button(self.main_container.width / 2 - 32, 320, 64, 64, (48, 48, 48), (64, 64, 64), (96, 96, 96),
                   self.button_action_4)
        ]

        for button in self.buttons:
            self.main_container.add_container(button)

    def draw(self, display):
        for button in self.buttons:
            button.update(self.mouse_pos)
        self.draw_selections()
        self.main_container.draw(display)

    def draw_selections(self):
        if self.preview_tile_pos:
            x, y = self.preview_tile_pos
            if self.tool == "selection":
                self.world.draw_tile_frame(self.display, self.camera, x, y, color=(192, 192, 192))
                if self.selected_tile_pos and self.selected_tile:
                    x, y = self.selected_tile_pos
                    self.world.draw_tile_frame(self.display, self.camera, x, y, color=(255, 0, 0))

            if self.tool == "building":
                if self.tile_map.get_tile(x, y):
                    self.world.draw_tile_frame(self.display, self.camera, x, y, color=(127, 255, 0))
                else:
                    self.world.draw_tile(self.display, self.camera, x, y, self.preview_tile, alpha=48)

            if self.tool == "multi_selection" or self.tool == "line_selection":
                color = (127, 196, 255) if self.tool == "multi_selection" else (255, 127, 0)
                if self.start_selection_tile_pos and self.end_selection_tile_pos:
                    start_x, start_y = self.start_selection_tile_pos
                    end_x, end_y = self.end_selection_tile_pos
                    self.world.draw_tile_area_frame(self.display, self.camera, start_x, start_y, end_x, end_y, color=color)

    def update_selections(self):
        if self.mouse_button_left:
            if self.tool == "multi_selection":
                self.end_selection_tile_pos = self.preview_tile_pos
            elif self.tool == "line_selection":
                if self.start_selection_tile_pos:
                    x, y = self.preview_tile_pos
                    start_x, start_y = self.start_selection_tile_pos

                    diff_x = abs(x - start_x)
                    diff_y = abs(y - start_y)

                    if diff_x > diff_y:
                        self.end_selection_tile_pos = (x, start_y)
                    else:
                        self.end_selection_tile_pos = (start_x, y)

    def update_preview_pos(self):
        x, y = self.mouse_pos
        world_pos = self.camera.screen_to_world(x, y, self.display.get_width() // 2, self.display.get_height() / 2,
                                                self.tile_size)
        x, y = world_pos
        self.preview_tile_pos = x, y

    def select_tile(self):
        x, y = self.mouse_pos
        world_pos = self.camera.screen_to_world(x, y, self.display.get_width() // 2, self.display.get_height() / 2,
                                                self.tile_size)
        x, y = world_pos
        self.selected_tile_pos = x, y
        self.selected_tile = self.tile_map.get_tile(x, y)

    def place_tile(self):
        if self.tool == "building":
            if self.selected_tile_pos:
                x, y = self.selected_tile_pos
                self.tile_map.set_tile(x, y, copy.copy(self.preview_tile))
        elif self.tool == "multi_selection" or self.tool == "line_selection":
            if self.start_selection_tile_pos and self.end_selection_tile_pos:
                start_x, start_y = self.start_selection_tile_pos
                end_x, end_y = self.end_selection_tile_pos
                self.place_tile_area(start_x, start_y, end_x, end_y, self.preview_tile)

    def place_tile_area(self, start_x, start_y, end_x, end_y, tile):

        if start_x > end_x:
            temp = start_x
            start_x = end_x
            end_x = temp

        if start_y > end_y:
            temp = start_y
            start_y = end_y
            end_y = temp

        for x in range(start_x, end_x+1):
            for y in range(start_y, end_y+1):
                tile_copy = copy.copy(tile)
                self.tile_map.set_tile(x, y, tile_copy)

    def rotate_preview_tile(self):
        self.preview_tile.rotation = (self.preview_tile.rotation + 1) % 4

    def button_action_1(self):
        self.tool = "selection"

    def button_action_2(self):
        self.tool = "building"

    def button_action_3(self):
        self.tool = "multi_selection"

    def button_action_4(self):
        self.tool = "line_selection"

    def handle_events(self, event):
        self.mouse_pos = pygame.mouse.get_pos()
        self.update_preview_pos()
        self.update_selections()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.place_tile()
            elif event.key == pygame.K_r:
                self.rotate_preview_tile()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                self.mouse_button_right = True
            elif event.button == 1:
                self.mouse_button_left = True
                self.start_selection_tile_pos = self.preview_tile_pos
                self.end_selection_tile_pos = self.preview_tile_pos
                self.select_tile()
                for button in self.buttons:
                    button.press()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                self.mouse_button_right = False
            elif event.button == 1:
                self.mouse_button_left = False
                for button in self.buttons:
                    button.release()
        elif event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                self.camera.zoom_in()
            elif event.y < 0:
                self.camera.zoom_out()
        elif event.type == pygame.MOUSEMOTION:
            if self.mouse_button_right:
                dx, dy = event.rel
                self.camera.move(-dx, -dy)
