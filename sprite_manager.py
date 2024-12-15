import os
import time

import pygame


class SpriteManager:
    def __init__(self):
        self.time_elapsed = time.time()
        self.sprites = {}
        self.metadata = {}

    def load_sprite_sheet(self, sprite_folder, name, variantes, directions, speed):
        if name not in self.sprites:
            self.sprites[name] = []
            self.metadata[name] = {
                "variantes": variantes,
                "directions": directions,
                "speed": speed,
            }

        for variante in range(variantes):
            variante_sprites = []
            for direction in range(directions):
                filename = f"{name}-{variante}-{direction}.png"
                filepath = os.path.join(sprite_folder, filename)

                if os.path.exists(filepath):
                    sprite = pygame.image.load(filepath).convert_alpha()
                    variante_sprites.append(sprite)
                else:
                    print(f"Warning: Sprite file {filepath} not found!")
                    variante_sprites.append(None)  # Placeholder pour fichier manquant
            self.sprites[name].append(variante_sprites)

    def get_sprite(self, name, variante, frame):
        if name in self.sprites:
            if 0 <= variante < len(self.sprites[name]) and 0 <= frame < len(self.sprites[name][variante]):
                return self.sprites[name][variante][frame]
        return None

    def get_animation_frame(self, name, variante):
        if name in self.metadata:
            directions = self.metadata[name]["directions"]
            speed = self.metadata[name]["speed"]
            frame = int((self.time_elapsed * speed) % directions)
            return self.get_sprite(name, variante, frame)

    def update_animation_frame(self):
        self.time_elapsed = time.time()