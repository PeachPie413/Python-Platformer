from core_classes import *
import physics.physics as physics
import world_data.globals as world_data_globals
import world_data.world_data as world_data



#=========================================================================================================================
#VARIABLES
#=========================================================================================================================


_chunk_colliders = {}
'''keeps track of the colliders created for each chunk'''



#=========================================================================================================================
#FUNCTIONS
#=========================================================================================================================



def create_colliders(chunk_pos = Vector2()):
    '''create colliders for a chunk'''
    global _chunk_colliders

    #if chunk does not exist then skip
    if chunk_pos.as_tuple() not in world_data_globals.zone_dict['overworld'].chunks:
        print('chunk ' + str(chunk_pos.as_tuple()) + ' does not exist!')
        return

    #get chunk
    chunk = world_data_globals.zone_dict['overworld'].chunks[chunk_pos.as_tuple()]
    chunk: world_data.Chunk
    tiles = chunk.tile_data

    #list of tiles taken in the chunk
    taken_tiles = []

    #pos in the chunk to start doing greedy things
    start_pos = Vector2()

    #while the tiles taken is not all the tiles in the chunk
    while len(taken_tiles) < world_data.CHUNK_SIZE * world_data.CHUNK_SIZE:

        #get tile
        tile = tiles.get_cell(start_pos.x, start_pos.y)
        tile: world_data.Tile

        #skip if tile is invalid
        if tile is None or tile.tile_type.collides is False:
            taken_tiles.append(start_pos.as_tuple())
            start_pos = _advance_pos(start_pos)
            continue


        #take horizontally
        end_pos = _take_horizontally(start_pos, tiles, taken_tiles)

        print(str(start_pos.as_tuple()) + ' ' + str(end_pos.as_tuple()))

        start_pos = _advance_pos(end_pos)


def _advance_pos(pos = Vector2()):
    '''move a position inside a chunk along to the next pos'''

    pos.x += 1

    if(pos.x >= world_data_globals.CHUNK_SIZE):
        pos.x = 0
        pos.y += 1

    return pos


def _take_horizontally(start_pos = Vector2(), tiles = Grid(), taken_tiles = []):
    '''try to take as many tiles as possile in a row, claiming the ones it takes, and returning the pos of the last tile it took'''

    current_pos = Vector2(start_pos.x, start_pos.y)

    #keep going until hit the end of the chunk
    while current_pos.x < world_data_globals.CHUNK_SIZE:

        tile = tiles.get_cell(start_pos.x + 1, start_pos.y)

        #stop if tile is none, in taken tiles, or not want a collider
        if tile is None or tile.tile_type.collides == False or current_pos.as_tuple() in taken_tiles:
            break

        #add tile to taken tiles and move forward by 1
        taken_tiles.append(current_pos.as_tuple())

        current_pos.x += 1

    #return last taken pos, but minus 1
    current_pos.x -= 1
    return current_pos


def _take_vertically(left_pos = Vector2(), right_pos = Vector2(), tiles = Grid(), taken_tiles = []):
    '''try to take as many tiles upwards as possible in a row, returns the right tile of the row it last took'''


def _create_collider(bottom_left = Vector2(), top_right = Vector2()):
    '''return a collider that covers the given tiles'''




def destroy_colliders(chunk_pos = Vector2()):
    '''destroy colliders for a chunk'''


def init():
    '''add the correct functions to the correct events'''