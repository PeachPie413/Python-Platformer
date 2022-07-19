from pygame import Vector2


class Position(Vector2):
    pass

class Vector2():
    def __init__(self) -> None:
        self.x = 0.0
        self.y = 0.0

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)