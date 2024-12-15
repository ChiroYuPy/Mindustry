import time

import pygame

from item import Item


class Tile:
    def __init__(self, variant=0):
        self.variant = variant
        self.max_variant = 1

    def get_image(self, sprite_manager):
        image = sprite_manager.get_animation_frame("Default", self.variant)
        return image

    def __repr__(self):
        return f"Tile({self.variant})"

    def to_dict(self):
        return {"variant": self.variant}

    @classmethod
    def from_dict(cls, data):
        return cls(data["variant"])


class DirectionalTile(Tile):
    def __init__(self, variant=0, direction=0):
        super().__init__(variant)
        self.direction = direction
        self.max_direction = 1

    def to_dict(self):
        return {"variant": self.variant, "direction": self.direction}


class Conveyer(DirectionalTile):
    def __init__(self, variant=0, direction=0):
        super().__init__(variant, direction)
        self.max_direction = 4
        self.max_variant = 5

    def get_image(self, sprite_manager):
        image = sprite_manager.get_animation_frame("conveyor", self.variant)
        image = pygame.transform.rotate(image, self.direction*90)
        return image

    def to_dict(self):
        return super().to_dict()

    @classmethod
    def from_dict(cls, data):
        return cls(data["variant"], data["direction"])


class BasicConveyer(Conveyer):
    def get_image(self, sprite_manager):
        image = sprite_manager.get_animation_frame("conveyor", self.variant)
        image = pygame.transform.rotate(image, self.direction*90)
        return image

class ArmoredConveyer(Conveyer):
    def get_image(self, sprite_manager):
        image = sprite_manager.get_animation_frame("armored-conveyor", self.variant)
        image = pygame.transform.rotate(image, self.direction*90)
        return image

class TitaniumConveyer(Conveyer):
    def get_image(self, sprite_manager):
        image = sprite_manager.get_animation_frame("titanium-conveyor", self.variant)
        image = pygame.transform.rotate(image, self.direction*90)
        return image

class Starter(DirectionalTile):
    def __init__(self, variant=0):
        super().__init__(variant)
        self.accumulator = 0
        self.max_direction = 4
        self.max_variant = 1

    def get_image(self, sprite_manager):
        image = sprite_manager.get_animation_frame("starter", self.variant)
        return image

    @property
    def direction(self):
        return self.variant

    def to_dict(self):
        return super().to_dict()

    @classmethod
    def from_dict(cls, data):
        return cls(data["variant"])

    def update(self, game, x, y, dt):
        self.accumulator += dt
        if self.accumulator >= 1:
            self.accumulator -= 1
            game.add_item(Item(x, y))