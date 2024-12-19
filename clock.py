import time


class Clock:
    def __init__(self):
        self.tick = 0
        self.total_time = 0
        self.current_time = time.time()

    def update(self, fps):
        last_time = self.current_time
        self.current_time = time.time()
        delta_time = self.current_time - last_time
        self.total_time += delta_time
        self.tick = int(self.total_time * 60)

        return delta_time
