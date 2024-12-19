import pygame

directions_pos = {
    0: (1, 0),
    1: (0, -1),
    2: (-1, 0),
    3: (0, 1),
}


class Tile:
    MAX_VARIANT = 0

    def __init__(self, variant=0):
        self.variant = variant

    def get_image(self, sprite_manager):
        raise ValueError("This method must be implemented in child class")

    def __repr__(self):
        return f"Tile({self.variant})"

    def to_dict(self):
        return {"variant": self.variant}

    @classmethod
    def from_dict(cls, data):
        return cls(data["variant"])


class UpdatedTile(Tile):
    MAX_DIRECTION = 0

    def __init__(self, variant=0):
        super().__init__(variant)
        self.accumulator = 0
        self.interval = 1

    def update(self, game, x, y, dt):
        self.accumulator += dt
        if self.accumulator >= self.interval:
            self.accumulator -= self.interval
            self.schedule(game, x, y, dt)

    def schedule(self, game, x, y, dt):
        self.update(game, x, y, dt)


class AnimatedTile(UpdatedTile):
    def __init__(self, variant=0):
        super().__init__(variant)
        self.animation = 0
        self.max_animation = 0
        self.animation_speed = 0

    def update(self, game, x, y, dt):
        super().update(game, x, y, dt)
        self.animation = (self.accumulator * self.animation_speed) % self.max_animation


class DirectionalTile(AnimatedTile):
    MAX_DIRECTION = 0

    def __init__(self, variant=0, direction=0):
        super().__init__(variant)
        self.direction = direction

    def to_dict(self):
        return {"variant": self.variant, "direction": self.direction}


class Conveyer(DirectionalTile):
    MAX_ANIMATION = 4
    MAX_DIRECTION = 4
    MAX_VARIANT = 5
    SPEED = 1

    def __init__(self, variant=0, direction=0):
        super().__init__(variant, direction)
        self.item = None
        self.interval = 1/self.SPEED
        self.max_animation = self.MAX_ANIMATION
        self.animation_speed = self.SPEED
        self.progress = 0

    def schedule(self, game, x, y, dt):
        x += directions_pos[self.direction][0]
        y += directions_pos[self.direction][1]
        print(directions_pos[self.direction])
        next_tile = game.tile_map[(x, y)]

        if next_tile and not next_tile.item:
            next_tile.item = self.item
        self.item = None

    def update(self, game, x, y, dt):
        super().update(game, x, y, dt)
        if self.item:
            next_tile = game.tile_map[(x, y)]
            if next_tile:
                self.progress = self.accumulator % self.interval * self.SPEED
        else:
            self.accumulator = 0

        if self.item:
            self.item.x = x + directions_pos[self.direction][0] * self.progress
            self.item.y = y + directions_pos[self.direction][1] * self.progress

    def get_image(self, sprite_manager):
        raise ValueError("This method must be implemented in child class")

    def to_dict(self):
        return {"variant": self.variant, "direction": self.direction}

    @classmethod
    def from_dict(cls, data):
        return cls(data["variant"], data["direction"])


class BasicConveyer(Conveyer):
    def __init__(self, variant=0, direction=0):
        super().__init__(variant, direction)

    def get_image(self, sprite_manager):

        image = sprite_manager.get_animation_frame("conveyor", self.variant)
        image = pygame.transform.rotate(image, self.direction*90)
        return image

class ArmoredConveyer(Conveyer):
    def __init__(self, variant=0, direction=0):
        super().__init__(variant, direction)

    def get_image(self, sprite_manager):
        image = sprite_manager.get_animation_frame("armored-conveyor", self.variant)
        image = pygame.transform.rotate(image, self.direction*90)
        return image

class TitaniumConveyer(Conveyer):
    def __init__(self, variant=0, direction=0):
        super().__init__(variant, direction)

    def get_image(self, sprite_manager):
        image = sprite_manager.get_animation_frame("titanium-conveyor", self.variant)
        image = pygame.transform.rotate(image, self.direction*90)
        return image

class Starter(DirectionalTile):
    MAX_DIRECTION = 4
    MAX_VARIANT = 1

    def __init__(self, variant=0):
        super().__init__(variant)

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
        pass