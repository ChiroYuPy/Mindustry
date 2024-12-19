class TileEntity:
    def __init__(self):
        self.items = []


class ConveyorTE(TileEntity):
    SPEED = 1

    def __init__(self, direction=0):
        super().__init__()
        self.direction = direction

    def rotate(self):
        self.direction = (self.direction + 1) % 4

    def update(self, world, x, y):
        if not self.items:
            return

        self.rotate()

        dx, dy = 0, 0
        if self.direction == 0:
            dy -= 1
        elif self.direction == 1:
            dx += 1
        elif self.direction == 2:
            dy += 1
        elif self.direction == 3:
            dx -= 1

        nx, ny = x + dx, y + dy

        next_tile = world.get_tile(nx, ny)
        if next_tile and next_tile.tile_entity and isinstance(next_tile.tile_entity, ConveyorTE):
            item = self.items.pop(0)
            next_tile.tile_entity.items.append(item)
