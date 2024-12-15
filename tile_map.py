import json

from tile import Starter, Conveyer, Tile


class TileMap:
    def __init__(self):
        self._tiles = {}

    def __getitem__(self, tile_pos):
        return self._tiles.get(tile_pos, None)

    def __setitem__(self, tile_pos, tile):
        self._tiles[tile_pos] = tile

    def __contains__(self, tile_pos):
        return tile_pos in self._tiles

    def __repr__(self):
        return f"{self.__class__.__name__}(Tiles: {len(self._tiles)})"

    def clear(self):
        self._tiles.clear()

    def items(self):
        return self._tiles.items()

    def save(self, filename):
        data = {
            "tiles": [
                {"x": x, "y": y, "tile": self.tile_to_dict(tile)} for (x, y), tile in self._tiles.items()
            ],
        }
        with open(filename, "w") as f:
            json.dump(data, f)

    def load(self, filename):
        with open(filename, "r") as f:
            data = json.load(f)
        self._tiles = {
            (tile_data["x"], tile_data["y"]): self.create_tile_from_dict(tile_data["tile"])
            for tile_data in data["tiles"]
        }

    @classmethod
    def tile_to_dict(cls, tile):
        if isinstance(tile, Conveyer):
            return {"type": "Conveyer", "direction": tile.direction}
        elif isinstance(tile, Starter):
            return {"type": "Starter", "direction": tile.direction}
        else:
            return {"type": "Tile", "direction": tile.direction}

    @classmethod
    def create_tile_from_dict(cls, tile_data):
        tile_type = tile_data["type"]
        if tile_type == "Conveyer":
            return Conveyer.from_dict(tile_data)
        elif tile_type == "Starter":
            return Starter.from_dict(tile_data)
        else:
            return Tile.from_dict(tile_data)
