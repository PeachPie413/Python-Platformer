from math import floor


class Vector2():
    def __init__(self, x = 0.0, y = 0.0) -> None:
        self.x = x
        self.y = y

    def __add__(self, other):
        if type(other) == float or type(other) is int:
            return Vector2(self.x + other, self.y + other)
        elif type(other) == Vector2:
            return Vector2(self.x + other.x, self.y + other.y)
        elif type(other) == tuple:
            return Vector2(self.x + other[0], self.y + other[1])

    def __radd__(other, self):
        if type(self) == float or type(self) == int:
            return Vector2(self.x + other, self.y + other)
        elif type(self) == Vector2:
            return Vector2(self.x + other.x, self.y + other.y)
        elif type(self) == tuple:
            return Vector2(other.x + self[0], other.y + self[1])

    def __sub__(self, other):
        if type(other) == float:
            return Vector2(self.x - other, self.y - other)
        elif type(other) == Vector2:
            return Vector2(self.x - other.x, self.y - other.y)

    def __rsub__(other, self):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if type(other) == float or type(other) == int:
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

    def __str__(self) -> str:
        return str(self.as_tuple())

    def as_tuple(self):
        return (self.x, self.y)


class Position():
    def __init__(self, vector = Vector2(0,0)):
        self.vector = vector



class Grid():
    def __init__(self, width = 3, height = 3, fill_data = None) -> None:
        self.width = width
        self.height = height
        self.data = []
        #fill data with None
        for i in range(width * height):
            self.data.append(fill_data)


    '''get the linear pos from xy coords, returns None if out of bounds'''
    def xy_to_linear(self, x = 0, y = 0):
        linear_pos = x + (y * self.height)

        if linear_pos >= len(self.data):
            return None
        else:
            return int(linear_pos)


    '''get the xy coords from a linear pos as an (x,y) tuple, returns none if out of bounds'''
    def linear_to_xy(self, n = 0):
        x = n % self.width
        y = floor(n / self.width)

        if x >= self.width or y >= self.height:
            return None
        else:
            return (x,y)


    '''set a cell in the grid using x,y coordinates. not passing any data to set automatically sets no data'''
    def set_cell(self, x = 0, y = 0, cell_data = None):
        #linear pos
        linear_pos = self.xy_to_linear(x,y)

        #return False if out of bounds
        if linear_pos == None:
            return False
        else:
            self.data[linear_pos] = cell_data

    '''get the data from a cell in the grid, returns none if out of bounds'''
    def get_cell(self, x = 0, y = 0):

        #get linear pos, return False if out of bounds
        if (linear_pos := self.xy_to_linear(x,y)) == None:
            return None
        else:
            return self.data[linear_pos]