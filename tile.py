import time
from item import Item


class Tile:
    def __init__(self, direction):
        self.direction = direction

    def __repr__(self):
        return f"Tile({self.direction})"

    def to_dict(self):
        return {"direction": self.direction}

    @classmethod
    def from_dict(cls, data):
        return cls(data["direction"])


class Starter(Tile):
    def __init__(self, direction):
        super().__init__(direction)
        self.last_item_time = time.time()

    def to_dict(self):
        return super().to_dict()

    @classmethod
    def from_dict(cls, data):
        return cls(data["direction"])

    def update(self, game, x, y):
        current_time = time.time()
        if current_time - self.last_item_time >= 1:
            game.add_item(Item(x, y))
            print(1)
            self.last_item_time = current_time


class Conveyer(Tile):
    def __init__(self, direction):
        super().__init__(direction)

    def to_dict(self):
        return super().to_dict()

    @classmethod
    def from_dict(cls, data):
        return cls(data["direction"])