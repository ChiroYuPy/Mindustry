class TileMap:
    def __init__(self):
        self.tiles = {}

    def place_tile(self, x, y, tile):
        self.tiles[(x, y)] = tile

    def delete_tile(self, x, y):
        del self.tiles[(x, y)]

    def get_tile(self, x, y):
        return self.tiles.get((x, y))

    def update(self):
        for (x, y), tile in self.tiles.items():
            if tile.tile_entity:
                tile.tile_entity.update(self, x, y)


