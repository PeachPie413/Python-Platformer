from core_classes import *
from world_data.globals import *
import esper as e




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

        self.tile_data = Grid(CHUNK_SIZE, CHUNK_SIZE, None)
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



def world_pos_to_chunk(world_pos = Vector2()):
    global CHUNK_SIZE

    return Vector2(floor(world_pos.x / CHUNK_SIZE), floor(world_pos.y / CHUNK_SIZE))


def chunk_pos_to_world(chunk_pos = Vector2()):
    global CHUNK_SIZE

    return chunk_pos * CHUNK_SIZE


def get_chunk_from_chunk_pos(chunk_pos = Vector2(), zone_id = 'overworld'):
    if zone_id in zone_dict:
        zone = zone_dict[zone_id]
        if chunk_pos.as_tuple() in zone.chunks:
            return zone.chunks[chunk_pos.as_tuple()]

    return None


def create_chunk(chunk_pos = Vector2(), zone_id = 'overworld'):
    global zone_dict
    global CHUNK_CREATED_EVENT_NAME

    #check if zone is in dict
    zone = None
    if zone_id not in zone_dict:
        zone = Zone(zone_id)
        zone_dict[zone_id] = zone
    #get zone
    else:
        zone = zone_dict[zone_id]

    #if chunk not in zone then create it
    if chunk_pos not in zone.chunks:

        chunk = _load_chunk(chunk_pos, zone_id)
        zone.chunks[chunk_pos.as_tuple()] = chunk

        #raise event
        e.dispatch_event(CHUNK_CREATED_EVENT_NAME, chunk_pos)

        #return created chunk
        return chunk


def destroy_chunk(chunk_pos = Vector2(), zone_id = 'overworld'):
    global zone_dict
    global CHUNK_DESTROYED_EVENT_NAME

    if zone_id in zone_dict:
        zone = zone_dict[zone_id]

        if chunk_pos.as_tuple() in zone.chunks:

            #destroy chunk
            _unload_chunk(zone.chunks[chunk_pos.as_tuple()], chunk_pos, zone_id)

            #remove from dicts
            del zone.chunks[chunk_pos.as_tuple()]

            #dispatch event
            e.dispatch_event(CHUNK_DESTROYED_EVENT_NAME, chunk_pos)





def _load_chunk(chunk_pos = Vector2(), zone_id = 'overworld'):
    return Chunk()


def _unload_chunk(chunk = Chunk(), chunk_pos = Vector2(), zone_id = 'overworld'):
    pass