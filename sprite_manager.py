import os
import time
import pygame
from config import TILE_SIZE

class SpriteManager:
    def __init__(self):
        self.time_elapsed = time.time()
        self.sprites = {}  # Stockage des sprites redimensionnés
        self.original_sprites = {}  # Stockage des sprites originaux
        self.metadata = {}

    def load_sprite_sheet(self, sprite_folder, name, variantes, frames, speed):
        if name not in self.sprites:
            self.sprites[name] = []
            self.original_sprites[name] = []  # Initialiser pour garder les versions originales
            self.metadata[name] = {
                "variantes": variantes,
                "frames": frames,
                "speed": speed,
            }

        for variante in range(variantes):
            variante_sprites = []
            variante_original_sprites = []
            for frame in range(frames):
                filename = f"{name}-{variante}-{frame}.png"
                filepath = os.path.join(sprite_folder, filename)

                if os.path.exists(filepath):
                    sprite = pygame.image.load(filepath).convert_alpha()
                    variante_original_sprites.append(sprite)  # Stocker la version originale
                    variante_sprites.append(sprite)  # On va redimensionner cette image plus tard
                else:
                    raise ValueError("Image Not Found")
            self.sprites[name].append(variante_sprites)
            self.original_sprites[name].append(variante_original_sprites)

    def get_sprite(self, name, variante, frame, resized=True):
        if name in self.sprites:
            if 0 <= variante < len(self.sprites[name]) and 0 <= frame < len(self.sprites[name][variante]):
                if resized:
                    return self.sprites[name][variante][frame]  # Version redimensionnée
                else:
                    return self.original_sprites[name][variante][frame]  # Version originale
        else:
            raise ValueError("Image not found!")

    def get_animation_frame(self, name, variant, resized=True):
        if name in self.metadata:
            frames = self.metadata[name]["frames"]
            speed = self.metadata[name]["speed"]
            frame = int((self.time_elapsed * speed) % frames)
            return self.get_sprite(name, variant, frame, resized)

    def update_animation_frame(self, zoom):
        self.time_elapsed = time.time()

        size = int(TILE_SIZE * zoom)
        for name in self.sprites:
            for variante in range(len(self.sprites[name])):
                for frame in range(len(self.sprites[name][variante])):
                    sprite = self.original_sprites[name][variante][frame]
                    if sprite:
                        self.sprites[name][variante][frame] = pygame.transform.scale(sprite, (size, size))
