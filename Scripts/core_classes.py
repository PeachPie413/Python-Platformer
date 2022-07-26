class Vector2():
    def __init__(self, x = 0.0, y = 0.0) -> None:
        self.x = x
        self.y = y

    def __add__(self, other):
        if type(other) == float:
            return Vector2(self.x + other, self.y + other)
        elif type(other) == Vector2:
            return Vector2(self.x + other.x, self.y + other.y)

    def __radd__(other, self):
        if type(self) == float or type(self) == int:
            return Vector2(self.x + other, self.y + other)
        elif type(self) == Vector2:
            return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if type(other) == float:
            return Vector2(self.x - other, self.y - other)
        elif type(other) == Vector2:
            return Vector2(self.x - other.x, self.y - other.y)

    def __rsub__(other, self):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if type(other) == float:
            return Vector2(self.x * other, self.y * other)

    def __truediv__(self, other):
        if type(other) == float:
            return Vector2(self.x / other, self.y / other)
        elif type(other) == Vector2:
            return Vector2(self.x / other.x, self.y / other.y)

    def __rtruediv__(other, self):
        if type(self) == float:
            return Vector2(self.x / other, self.y / other)
        elif type(self) == Vector2:
            return Vector2(self.x / other.x, self.y / other.y)


class Position():
    def __init__(self, vector = Vector2(0,0)):
        self.vector = vector