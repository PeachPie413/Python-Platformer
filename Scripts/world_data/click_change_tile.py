import world_data.world_data as world_data
import esper as e
import rendering.rendering as rendering
import resources.globals as resource_globals



#================================================================================
#VARIABLES
#================================================================================







#================================================================================
#FUNCTIONS
#================================================================================



def _place_tile_at_mouse_pos(tile_type_id = 'stone'):
    '''sets tile data at the tile the mouse is over'''
    global _place_tile_type_name

    mouse_pos = rendering.get_mouse_world_pos()

    #get chunk
    chunk = world_data.get_chunk_mouse_is_in()
    if chunk is None:
        return

    chunk: world_data.Chunk

    #set tile
    tile = None
    if tile_type_id is not None:
        tile = world_data.Tile(resource_globals.tile_type_dict[tile_type_id], world_data.world_to_tile(mouse_pos))
    chunk.set_tile(mouse_pos, tile)