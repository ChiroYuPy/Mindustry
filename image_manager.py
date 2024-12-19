import os
import pygame


class ImageManager:
    def __init__(self, base_path):
        self.resized_animations = {}
        self.resized_images = {}
        self.base_path = base_path
        self.images = {}
        self.animations_fps = {}

    def load_image(self, tile_type, image_path):
        self.images[tile_type] = pygame.image.load(os.path.join(self.base_path, image_path))

    def load_animation(self, tile_type, folder_path, fps=10):
        path = os.path.join(self.base_path, folder_path)
        image_files = [f for f in os.listdir(path) if f.endswith('.png')]
        image_files.sort()

        self.images[tile_type] = [pygame.image.load(os.path.join(path, img)) for img in image_files]
        self.animations_fps[tile_type] = fps

    def get_image(self, tile_type, frame=0, rotation=0):
        asset = self.resized_animations.get(tile_type) or self.resized_images.get(tile_type) or self.images.get(
            tile_type)

        if isinstance(asset, list):
            fps = self.animations_fps.get(tile_type, 10)
            frame_index = (frame // (60 // fps)) % len(asset)
            image = asset[frame_index]
        else:
            image = asset

        if rotation > 0:
            image = pygame.transform.rotate(image, -90 * rotation)

        return image

    def resize(self, tile_size):
        self.resized_images = {}
        self.resized_animations = {}

        for tile_type, asset in self.images.items():
            print(asset)
            if isinstance(asset, list):
                self.resized_animations[tile_type] = [
                    pygame.transform.scale(image, (tile_size, tile_size)) for image in asset
                ]
            else:
                self.resized_images[tile_type] = pygame.transform.scale(asset, (tile_size, tile_size))
                print(self.resized_images[tile_type])
