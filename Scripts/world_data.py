from core_classes import *
import global_variables as gb
import esper as e



CHUNK_SIZE = 32
CHUNK_CHANGED_EVENT_NAME = 'chunk_changed'
CHUNK_CREATED_EVENT_NAME = 'chunk_loaded'
CHUNK_DESTROYED_EVENT_NAME = 'chunk_destroyed'

zone_dict = {}



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

    
    def get_tile(self, world_pos):
        pass


    def set_tile(self, world_pos):
        pass





class Zone:
    def __init__(self, id = 'overworld') -> None:
        self.id = id
        self.chunks = {} # for key in chunks use tuple version of chunk pos



def world_pos_to_chunk



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
        zone.chunks[chunk_pos.as_tuple()] = _load_chunk(chunk_pos, zone_id)

        #raise event
        e.dispatch_event(CHUNK_CREATED_EVENT_NAME, chunk_pos)

def destroy_chunk(chunk_pos = Vector2(), zone_id = 'overworld'):
    global zone_dict
    global CHUNK_DESTROYED_EVENT_NAME

    if zone_id in zone_dict:
        zone = zone_dict[zone_id]

        print(zone.chunks)
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