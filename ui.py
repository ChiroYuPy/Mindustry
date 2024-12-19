import pygame


class Widget:
    def __init__(self, x, y, width, height):
        self._relative_pos = pygame.Vector2(x, y)
        self._rect = pygame.Rect(x, y, width, height)
        self._hovered = False

    def draw(self, surface):
        raise ValueError("This method must be overridden")

    def update_position(self, parent_pos):
        self._rect.x = parent_pos.x + self._relative_pos.x
        self._rect.y = parent_pos.y + self._relative_pos.y

    def is_hover(self, mouse_pos):
        self._hovered = self._rect.collidepoint(mouse_pos)


class Button(Widget):
    def __init__(self, x, y, width, height, color, hover_color, press_color, action=None):
        super().__init__(x, y, width, height)
        self._action = action
        self._color = color
        self._hover_color = hover_color
        self._press_color = press_color
        self._pressed = False

    def draw(self, surface):
        if self._hovered:
            if self._pressed:
                color = self._press_color
            else:
                color = self._hover_color
        else:
            color = self._color
        pygame.draw.rect(surface, color, self._rect)

    def update(self, mouse_pos):
        self.is_hover(mouse_pos)

    def trigger_action(self):
        if self._action:
            self._action()

    def press(self):
        if not self._pressed:
            self._pressed = True
            if self._hovered:
                self.trigger_action()

    def release(self):
        self._pressed = False


class Container:
    def __init__(self, x, y, width, height, color):
        self._relative_pos = pygame.Vector2(x, y)
        self._rect = pygame.Rect(x, y, width, height)
        self._color = color
        self._widgets = []
        self._containers = []

    @property
    def x(self):
        return self._rect.x

    @property
    def y(self):
        return self._rect.y

    @property
    def width(self):
        return self._rect.width

    @property
    def height(self):
        return self._rect.height

    def add_widget(self, widget):
        self._widgets.append(widget)

    def add_container(self, container):
        self._containers.append(container)

    def draw(self, surface):
        self.update_position()
        pygame.draw.rect(surface, self._color, self._rect)
        for widget in self._widgets:
            widget.draw(surface)
        for container in self._containers:
            container.draw(surface)

    def update_position(self, parent_pos=None):
        if parent_pos:
            self._rect.x = parent_pos.x + self._relative_pos.x
            self._rect.y = parent_pos.y + self._relative_pos.y
        for widget in self._widgets:
            widget.update_position(self._rect)
        for container in self._containers:
            container.update_position(self._rect)
