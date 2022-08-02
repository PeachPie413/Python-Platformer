from core_classes import *
import global_variables as gb



CHUNK_SIZE = 32
CHUNK_CHANGED_EVENT_NAME = 'chunk_changed'
CHUNK_CREATED_EVENT_NAME = 'chunk_loaded'
CHUNK_DESTROYED_EVENT_NAME = 'chunk_destroyed'

zone_dict = {}


def create_chunk(chunk_pos = Vector2(), zone_id = 'overworld'):
    global zone_dict

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
        zone.chunks[chunk_pos] = _load_chunk(chunk_pos, zone_id)

def destroy_chunk(chunk_pos = Vector2(), zone_id = 'overworld'):
    pass


def _load_chunk(chunk_pos = Vector2(), zone_id = 'overworld'):
    return Chunk()



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

        self.tile_data = Grid(CHUNK_SIZE, CHUNK_SIZE)
        self.pos = chunk_pos

class Zone:
    def __init__(self, id = 'overworld') -> None:
        self.id = id
        self.chunks = {}