from core_classes import *
import global_variables as gb
import esper as e
import resources
from world_data.classes import *


CHUNK_SIZE = 32
CHUNK_CHANGED_EVENT_NAME = 'chunk_changed'
CHUNK_CREATED_EVENT_NAME = 'chunk_loaded'
CHUNK_DESTROYED_EVENT_NAME = 'chunk_destroyed'

zone_dict = {}



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
        zone.chunks[chunk_pos.as_tuple()] = _load_chunk(chunk_pos, zone_id)

        #raise event
        e.dispatch_event(CHUNK_CREATED_EVENT_NAME, chunk_pos)


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