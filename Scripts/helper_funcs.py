from core_classes import *

def get_positions_in_square(radius = 0, center = Vector2()):
    '''get a list of positions within a square, with a side length of radius * 2 + 1, and a center of center'''

    positions = []

    for x in range(int(center.x - radius), int(center.x + radius + 1)): 
        for y in range(int(center.y - radius), int(center.y + radius + 1)): 
            positions.append(Vector2(x,y))

    return positions