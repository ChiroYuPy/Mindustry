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
        print("clear")
        self._tiles.clear()

    def items(self):
        return self._tiles.items()

    def save(self, filename):
        print("save")
        data = {
            "tiles": [
                {"x": x, "y": y, "tile": self.tile_to_dict(tile)} for (x, y), tile in self._tiles.items()
            ],
        }
        with open(filename, "w") as f:
            json.dump(data, f)

    def load(self, filename):
        print("load")
        with open(filename, "r") as f:
            data = json.load(f)
        self._tiles = {
            (tile_data["x"], tile_data["y"]): self.create_tile_from_dict(tile_data["tile"])
            for tile_data in data["tiles"]
        }

    @staticmethod
    def clear_file(filename):
        with open(filename, "w") as f:
            json.dump({}, f)

    @classmethod
    def tile_to_dict(cls, tile):
        return {"type": type(tile).__name__, "variant": tile.variant}

    @classmethod
    def create_tile_from_dict(cls, tile_data):
        tile_type = tile_data["type"]
        if tile_type == "Conveyer":
            return Conveyer.from_dict(tile_data)
        elif tile_type == "Starter":
            return Starter.from_dict(tile_data)
        else:
            return Tile.from_dict(tile_data)
