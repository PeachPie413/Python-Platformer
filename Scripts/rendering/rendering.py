from core_classes import *
from rendering.globals import *
import global_variables as gb
import pygame as py
import esper as e
import resources.globals as resources
import world_data.world_data as world_data
import world_data.globals as world_data_globals


def init():
    set_camera_zoom()
    create_game_window()


#=========================================================================================================================
#PRIVATE VARIABLES
#=========================================================================================================================



_camera_height = 0
_camera_position = Vector2()
#background color, when nothing is being rendered
_screen_background_color = (255,255,255)
#scale for how many pixels in a sprite should be on unit long
_sprite_pix_to_world_scale = 8
_camera_width = 10.0


    
#=========================================================================================================================
#CLASSES
#=========================================================================================================================



class Renderable_Rect:
    def __init__(self, color = (255, 192, 203), width = 1.0, height = 1.0) -> None:
        self.color = color
        self.width = width
        self.height = height

class Sprite:
    def __init__(self, sprite_id = 0) -> None:
        self.sprite_id = sprite_id

class Camera_Follow:
    def __init__(self) -> None:
        pass



#=========================================================================================================================
#SCREEN FUNCTIONS
#=========================================================================================================================



'''create the native screen, the one that is not sclaed to screen'''
def set_native_screen():
    global native_render_surface
    global _camera_width
    global _camera_height
    global _sprite_pix_to_world_scale
    global _screen_background_color

    native_render_surface = py.Surface(
        (_camera_width * _sprite_pix_to_world_scale, _camera_height * _sprite_pix_to_world_scale)
    )

    native_render_surface.fill(_screen_background_color)

'''take the native screen and scale it to the game window'''
def scale_native_screen_to_window():
    global native_render_surface

    py.transform.scale(native_render_surface, (gb.SCREEN_WIDTH, gb.SCREEN_HEIGHT), gb.game_window)

'''get the native screen pos of a world pos'''
def _world_to_native_pos(world_pos = Vector2()):
    global _camera_position
    global _sprite_pix_to_world_scale
    global _camera_width
    global _camera_height

    native_pos = Vector2()
    native_pos.x = (world_pos.x - _camera_position.x + _camera_width / 2.0) * _sprite_pix_to_world_scale
    native_pos.y = (_sprite_pix_to_world_scale * _camera_height - ((world_pos.y - _camera_position.y + _camera_height / 2.0) * _sprite_pix_to_world_scale))

    return native_pos

'''create the game window'''
def create_game_window():
    gb.game_window = py.display.set_mode((gb.SCREEN_WIDTH, gb.SCREEN_HEIGHT))

'''set the width of the camera in world units'''
def set_camera_zoom(zoom = 10.0):
    if zoom < 10.0: zoom = 10.0

    global _camera_width
    global _camera_height
    global camera_zoom
    global world_to_pix_ratio

    camera_zoom = zoom
    _camera_width = zoom
    _camera_height = zoom / gb.SCREEN_WIDTH_TO_HEIGHT_RATIO

    #reset world to pix ratio
    world_to_pix_ratio = gb.SCREEN_WIDTH / _camera_width



#=========================================================================================================================
#TILEMAP RENDERING
#=========================================================================================================================



def render_tilemaps():
    global native_render_surface
    global _world_to_native_pos

    #go through all chunks
    for chunk in world_data_globals.zone_dict['overworld'].chunks.values():

        #get chunk bottom left pos
        chunk_world_pos = world_data.chunk_pos_to_world(chunk.chunk_pos)

        #go through tiles
        for i, tile in enumerate(chunk.tile_data.data):

            #skip tile if None
            if tile is None: continue

            #get tile world pos
            tile_pos = chunk.tile_data.linear_to_xy(i) + chunk_world_pos

            #blit to screen
            native_render_surface.blit(resources.sprite_list[tile.tile_type.sprite], _world_to_native_pos(tile_pos).as_tuple())


'''return chunks that are in the cameras view'''
def _get_chunks_to_render():
    pass



#=========================================================================================================================
#SPRITE RENDERING 
#=========================================================================================================================



def _render_sprites():
    global _get_sprites, _draw_sprites

    sprites = _get_sprites()

    _draw_sprites(sprites)

def _get_sprites():
    return gb.entity_world.get_components(Position, Sprite)

def _draw_sprites(sprites = []):
    global native_render_surface, _world_to_native_pos

    for ent, (pos, sprite) in sprites:

        #get native pos of sprite
        native_pos = _world_to_native_pos(pos.vector)

        #blit to native
        native_render_surface.blit(resources.sprite_list[sprite.sprite_id], native_pos.as_tuple())



#=========================================================================================================================
#PROCESSORS
#=========================================================================================================================



class Render_Processor(e.Processor):

    def process(self):
        global _world_to_native_pos, _render_sprites, render_tilemaps, scale_native_screen_to_window, set_native_screen


        set_native_screen()
        render_tilemaps()
        _render_sprites()

        scale_native_screen_to_window()
        py.display.flip()


class Follow_Camera_Processor(e.Processor):

    def process(self):
        global _camera_position

        camera_followers = gb.entity_world.get_components(Camera_Follow, Position)

        #if there is a camera follower then get the first one and use that
        if(len(camera_followers) > 0):
            ent, (camera_follow, pos) = camera_followers[0]
            _camera_position = pos.vector