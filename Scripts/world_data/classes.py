from core_classes import *
import resources
from world_data.functions import *

class Tile_Type:
    def __init__(self, id_name = 'tile-stone', sprite = 0, collides = False):
        self.id_name = id_name
        self.sprite = sprite
        self.collides = collides

class Tile:
    def __init__(self, tile_type = Tile_Type(), pos = Vector2()) -> None:
        self.tile_type = tile_type
        self.pos = pos

class Chunk:
    def __init__(self, chunk_pos = Vector2()) -> None:
        global CHUNK_SIZE

        self.tile_data = Grid(CHUNK_SIZE, CHUNK_SIZE, Tile(resources.tile_type_dict['stone']))
        self.chunk_pos = chunk_pos


    def _world_to_local_pos(self, world_pos):
        chunk_world_pos = chunk_pos_to_world(self.chunk_pos)

        #convert to local tile pos
        return Vector2(floor(world_pos.x - chunk_world_pos.x), floor(world_pos.y - chunk_world_pos.y))

    
    def get_tile(self, world_pos):

        local_tile_pos = self._world_to_local_pos(world_pos)       

        return self.tile_data.get_cell(local_tile_pos.x, local_tile_pos.y)


    def set_tile(self, world_pos, new_tile):
        global CHUNK_CHANGED_EVENT_NAME

        #change tile
        local_tile_pos = self._world_to_local_pos(world_pos)
        tile = self.tile_data.get_cell(local_tile_pos.x, local_tile_pos.y)

        #if tile is in grid
        if tile != None:
            tile = new_tile

            #raise event
            e.dispatch_event(CHUNK_CHANGED_EVENT_NAME, self.chunk_pos, local_tile_pos)



class Zone:
    def __init__(self, id = 'overworld') -> None:
        self.id = id
        self.chunks = {} # for key in chunks use tuple version of chunk pos