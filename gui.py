import pygame

from color import get_color
from config import TILE_SIZE


class GUI:
    WIDTH = 256
    HEIGHT = 128

    def __init__(self, editor):
        self.editor = editor
        self.font = pygame.font.SysFont("Arial", 24)
        self.surface = pygame.surface.Surface((self.WIDTH, self.HEIGHT)).convert_alpha()

    def draw(self, display):
        self.surface.fill((32, 32, 32, 127))
        text = self.font.render(f"Selected Tile: {self.editor.selected_tile_type}", True, (255, 255, 255))
        self.surface.blit(text, (10, 10))
        pygame.draw.rect(self.surface, get_color(self.editor.selected_tile_type), (10, 48, TILE_SIZE, TILE_SIZE))
        display.blit(self.surface, (0, 0))
