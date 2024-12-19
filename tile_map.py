class TileMap:
    def __init__(self):
        self.tiles = {}

    def place_tile_area(self, start_x, start_y, end_x, end_y, tile):
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                tile_copy = tile.copy()
                self.place_tile(x, y, tile_copy)

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
