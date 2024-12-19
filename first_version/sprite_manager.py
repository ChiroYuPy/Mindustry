import os
import time
import pygame
from config import TILE_SIZE


class SpriteManager:
    def __init__(self):
        self.time_elapsed = time.time()
        self.sprites = {}
        self.original_sprites = {}
        self.metadata = {}

        self.tree = {}
        self.build_tree_from_directory("assets")

    def _get_nested_dict(self, base_dict, path, create_missing=True):
        current = base_dict
        for part in path:
            if part not in current:
                if create_missing:
                    current[part] = {}
                else:
                    raise KeyError(f"Path {'/'.join(path)} does not exist.")
            current = current[part]
        return current

    def create_dictionary(self, path):
        keys = path.split(".")
        self._get_nested_dict(self.tree, keys)

    def add_image(self, path, image_path):
        keys = path.split(".")
        target_dict = self._get_nested_dict(self.tree, keys)
        if os.path.exists(image_path):
            target_dict['image'] = pygame.image.load(image_path).convert_alpha()
        else:
            raise FileNotFoundError(f"Image file {image_path} not found.")

    def build_tree_from_directory(self, base_folder):
        root_path = os.path.join(os.getcwd(), base_folder)

        for dirpath, dirnames, filenames in os.walk(root_path):
            relative_dir = os.path.relpath(dirpath, root_path)
            sub_keys = relative_dir.split(os.sep) if relative_dir != '.' else []
            current_dict = self._get_nested_dict(self.tree, sub_keys)

            for filename in filenames:
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    file_path = os.path.join(dirpath, filename)
                    image_key = os.path.splitext(filename)[0]
                    current_dict[image_key] = pygame.image.load(file_path).convert_alpha()

    def get_image(self, path):
        keys = path.split(".")
        target_dict = self._get_nested_dict(self.tree, keys, create_missing=False)
        if 'image' in target_dict:
            return target_dict['image']
        else:
            raise KeyError(f"No image found at path {path}")

    def load_sprite_sheet(self, sprite_folder, name, variantes, frames, speed):
        if name not in self.sprites:
            self.sprites[name] = []
            self.original_sprites[name] = []
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

        size = int(TILE_SIZE * zoom) + 1
        for name in self.sprites:
            for variante in range(len(self.sprites[name])):
                for frame in range(len(self.sprites[name][variante])):
                    sprite = self.original_sprites[name][variante][frame]
                    if sprite:
                        self.sprites[name][variante][frame] = pygame.transform.scale(sprite, (size, size))
