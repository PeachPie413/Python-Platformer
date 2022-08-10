from core_classes import *
import physics.physics as physics
import esper as e
import world_data.globals as world_data_globals
import world_data.world_data as world_data
import global_variables as gb



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

    #add chunk to collider dict
    created_colliders = []
    _chunk_colliders[chunk_pos.as_tuple()] = created_colliders

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

        #skip if tile is invalid
        if tile is None or tile.tile_type.collides is False:
            taken_tiles.append(start_pos.as_tuple())
            start_pos = _advance_pos(start_pos)
            continue


        #take horizontally
        end_pos = _take_horizontally(start_pos, tiles, taken_tiles)

        #take vertically
        end_pos = _take_vertically(start_pos, end_pos, tiles, taken_tiles)

        #create collider and add to created colliders
        collider_ent = _create_collider(start_pos, end_pos)
        created_colliders.append(collider_ent)

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

    current_elevation = right_pos.y

    #keep going until hit the top of chunk
    while current_elevation < world_data_globals.CHUNK_SIZE:

        current_elevation += 1

        #check from the row above the current one
        row_above_clear = True
        for x in range(int(left_pos.x), int(right_pos.x) + 1):

            #get tile
            tile = tiles.get_cell(x, current_elevation)

            #if tile is not available, then break and say row not clear
            if tile is None or tile.tile_type.collides == False or (x, current_elevation) in taken_tiles:
                row_above_clear = False
                break

        #if row is clear
        if row_above_clear:

            #claim the tiles in the row
            for x in range(int(left_pos.x), int(right_pos.x) + 1):
                taken_tiles.append((x, current_elevation))

        if not row_above_clear:

            #break loop
            break

    current_elevation -= 1

    return Vector2(right_pos.x, current_elevation)


def _create_collider(bottom_left = Vector2(), top_right = Vector2()):
    '''return a collider entity that covers the given tiles'''

    #uses pos of tile as bottom-left of tile, so add one to top-right
    top_right = top_right + 1

    #get center of collider
    center = (bottom_left + top_right) / 2.0

    #width and height
    width = top_right.x - bottom_left.x
    height = top_right.y - bottom_left.y

    #create entity
    collider_ent = gb.entity_world.create_entity(
        physics.Collider(width, height),
        Position(center)
    )

    return collider_ent


def destroy_colliders(chunk_pos = Vector2()):
    '''destroy colliders for a chunk'''


def recreate_colliders(chunk_pos = Vector2()):
    '''destroy then re-create the colliders for a chunk'''

    destroy_colliders(chunk_pos)
    create_colliders(chunk_pos)


def init():
    '''add the correct functions to the correct events'''
    global create_colliders, destroy_colliders, recreate_colliders

    #chunk changed
    e.set_handler(world_data_globals.CHUNK_CHANGED_EVENT_NAME, recreate_colliders)

    #chunk created
    e.set_handler(world_data_globals.CHUNK_CREATED_EVENT_NAME, create_colliders)

    #chunk destroyed
    e.set_handler(world_data_globals.CHUNK_DESTROYED_EVENT_NAME, destroy_colliders)