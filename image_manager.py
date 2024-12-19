import os
import pygame


class ImageManager:
    def __init__(self, base_path):
        self.base_path = base_path
        self.images = {}
        self.animations_fps = {}

    def load_image(self, tile_type, image_path):
        self.images[tile_type] = pygame.image.load(os.path.join(self.base_path + image_path))

    def load_animation(self, tile_type, folder_path, fps=10):
        path = os.path.join(self.base_path + folder_path)
        image_files = [f for f in os.listdir(path) if f.endswith('.png')]
        image_files.sort()

        self.images[tile_type] = [pygame.image.load(os.path.join(self.base_path, folder_path, img)) for img in image_files]
        self.animations_fps[tile_type] = fps

    def get_image(self, tile_type, frame=0, rotation=0):
        asset = self.images.get(tile_type)
        if isinstance(asset, list):
            fps = self.animations_fps.get(tile_type, 10)
            frame_index = (frame // (60 // fps)) % len(asset)
            image = asset[frame_index]
        else:
            image = asset

        if rotation > 0:
            image = pygame.transform.rotate(image, -90 * image)

        return image