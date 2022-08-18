from core_classes import *
from world_data.globals import *
import resources.globals as resources_globals
import esper as e
import pygame as py
import rendering.rendering as rendering




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
        '''set a tile in the chunk, takes world position'''
        global CHUNK_CHANGED_EVENT_NAME

        local_tile_pos = self._world_to_local_pos(world_pos)

        #if tile is in grid
        if self.tile_data.is_cell_in_grid(local_tile_pos.x, local_tile_pos.y):
            
            #set tile data
            self.tile_data.set_cell(local_tile_pos.x, local_tile_pos.y, new_tile)

            #raise event
            e.dispatch_event(CHUNK_CHANGED_EVENT_NAME, self.chunk_pos, local_tile_pos)




class Zone:
    def __init__(self, id = 'overworld') -> None:
        self.id = id
        self.chunks = {} # for key in chunks use tuple version of chunk pos



#=========================================================================================================================
#=========================================================================================================================
#POSITION FUNCTIONS
#=========================================================================================================================
#=========================================================================================================================



def world_pos_to_chunk(world_pos = Vector2()):
    global CHUNK_SIZE

    return Vector2(floor(world_pos.x / CHUNK_SIZE), floor(world_pos.y / CHUNK_SIZE))


def chunk_pos_to_world(chunk_pos = Vector2()):
    global CHUNK_SIZE

    return chunk_pos * CHUNK_SIZE


def get_chunk_from_chunk_pos(chunk_pos = Vector2(), zone_id = 'overworld'):
    if zone_id in zone_dict:
        zone = zone_dict[zone_id]
        if chunk_pos.to_tuple() in zone.chunks:
            return zone.chunks[chunk_pos.to_tuple()]

    return None


def world_to_tile(world_pos = Vector2()):
    '''take a world pos and get the world pos of the tile it's in'''
    return Vector2(
        floor(world_pos.x),
        floor(world_pos.y)
    )


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
        zone.chunks[chunk_pos.to_tuple()] = chunk

        #raise event
        e.dispatch_event(CHUNK_CREATED_EVENT_NAME, chunk_pos)

        #return created chunk
        return chunk


def destroy_chunk(chunk_pos = Vector2(), zone_id = 'overworld'):
    global zone_dict
    global CHUNK_DESTROYED_EVENT_NAME

    if zone_id in zone_dict:
        zone = zone_dict[zone_id]

        if chunk_pos.to_tuple() in zone.chunks:

            #destroy chunk
            _unload_chunk(zone.chunks[chunk_pos.to_tuple()], chunk_pos, zone_id)

            #remove from dicts
            del zone.chunks[chunk_pos.to_tuple()]

            #dispatch event
            e.dispatch_event(CHUNK_DESTROYED_EVENT_NAME, chunk_pos)


def create_chunks_in_square(chunk_pos = Vector2(), width = 10):
    '''create sum chunks in a square w/ the given radius, and whith the given pos at it's center'''
    global create_chunk

    half_width = width / 2

    #for all chunk position in a square
    for x in range(int(chunk_pos.x - half_width), int(chunk_pos.x + half_width)):
        for y in range(int(chunk_pos.y - half_width), int(chunk_pos.y + half_width)):
            create_chunk(Vector2(x,y))




def _load_chunk(chunk_pos = Vector2(), zone_id = 'overworld'):
    '''load a chunk, either from file or if not in file then generate it's data'''
    global _create_tile_data

    chunk = Chunk()
    chunk.chunk_pos = chunk_pos

    chunk.tile_data = _create_tile_data(chunk_pos)

    return chunk


def _unload_chunk(chunk = Chunk(), chunk_pos = Vector2(), zone_id = 'overworld'):
    pass



def get_chunk(chunk_pos = Vector2(), zone_id = 'overworld'):
    '''get a chunk from a chunk pos and a zone id'''
    global zone_dict

    if zone_id not in zone_dict:
        return None
    
    zone = zone_dict[zone_id]

    if chunk_pos.to_tuple() not in zone.chunks:
        return None

    return zone.chunks[chunk_pos.to_tuple()]



#=========================================================================================================================
#CHUNK CREATION FUNCTIONS
#=========================================================================================================================



def _create_tile_data(chunk_pos = Vector2()):
    '''create tile data (terrain gen) for a chunk, returns a grid of the tile data'''
    global CHUNK_SIZE, chunk_pos_to_world, _get_tile_debug_flat

    tile_data = Grid(CHUNK_SIZE, CHUNK_SIZE)
    chunk_world_pos = chunk_pos_to_world(chunk_pos)
    tile_type = resources_globals.tile_type_dict[DEBUG_WORLD_GEN_TILE_TYPE]

    for x in range(int(chunk_world_pos.x), int(chunk_world_pos.x) + CHUNK_SIZE):
        for y in range(int(chunk_world_pos.y), int(chunk_world_pos.y) + CHUNK_SIZE):

            tile = _get_tile_debug_flat(Vector2(x,y), tile_type)
            local_x = x - chunk_world_pos.x
            local_y = y - chunk_world_pos.y
            tile_data.set_cell(local_x, local_y, tile)

    return tile_data



def _get_tile_debug_flat(tile_pos = Vector2(), tile_type = Tile_Type()):
    '''world gen function for a debug flat world'''

    if tile_pos.y <= 0:
        return Tile(tile_type, tile_pos)
    else:
        return None



#=========================================================================================================================
#MISC HELPER FUNCTIONS
#=========================================================================================================================



def get_chunk_mouse_is_in():
    '''get the chunk that the mouse is currently in'''
    global world_pos_to_chunk, get_chunk

    #get mouse pos
    mouse_pos = rendering.get_mouse_world_pos()

    #turn to chunk pos
    chunk_pos = world_pos_to_chunk(mouse_pos)

    #get chunk
    return get_chunk(chunk_pos)




#=========================================================================================================================
#DEBUG FUNCTIONS
#=========================================================================================================================




def show_chunk_borders():
    '''render the borders of all chunks in the dict'''
    global zone_dict, CHUNK_BORDER_COLOR, CHUNK_SIZE, chunk_pos_to_world

    chunks = zone_dict['overworld'].chunks

    for chunk_pos in chunks:

        render_pos = chunk_pos_to_world(Vector2(chunk_pos[0], chunk_pos[1]))
        render_pos = render_pos + (CHUNK_SIZE / 2)

        #draw chunk
        rendering.draw_rect(
            rendering.Renderable_Rect(CHUNK_BORDER_COLOR, CHUNK_SIZE, CHUNK_SIZE, 3),
            render_pos
        )