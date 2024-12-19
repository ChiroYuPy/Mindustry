from copy import copy


class Tile:
    def __init__(self, tile_type, variant=None, rotation=0, tile_entity=None):
        self.tile_type = tile_type
        self.variant = variant
        self.rotation = rotation  # [0;3]
        self.tile_entity = tile_entity

    def is_active(self):
        return self.tile_entity is not None

    def __copy__(self):
        return Tile(self.tile_type, self.variant, self.rotation, copy(self.tile_entity))