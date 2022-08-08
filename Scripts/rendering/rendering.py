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
    def __init__(self, color = (255, 192, 203), width = 1.0, height = 1.0, border_width = 0) -> None:
        self.color = color
        self.width = width
        self.height = height
        self.border_width = border_width

class Sprite:
    def __init__(self, sprite_id = 0) -> None:
        self.sprite_id = sprite_id

class Camera_Follow:
    def __init__(self) -> None:
        pass



#=========================================================================================================================
#SCREEN FUNCTIONS
#=========================================================================================================================



def set_native_screen():
    '''create the native screen, the one that is not sclaed to screen'''

    global native_render_surface
    global _camera_width
    global _camera_height
    global _sprite_pix_to_world_scale
    global _screen_background_color

    native_render_surface = py.Surface(
        (_camera_width * _sprite_pix_to_world_scale, _camera_height * _sprite_pix_to_world_scale)
    )

    native_render_surface.fill(_screen_background_color)


def _scale_native_screen_to_window():
    '''take the native screen and scale it to the game window'''

    global native_render_surface

    py.transform.scale(native_render_surface, (gb.SCREEN_WIDTH, gb.SCREEN_HEIGHT), gb.game_window)


def _world_to_native_pos(world_pos = Vector2()):
    '''get the native screen pos of a world pos'''

    global _camera_position
    global _sprite_pix_to_world_scale
    global _camera_width
    global _camera_height

    native_pos = Vector2()
    native_pos.x = (world_pos.x - _camera_position.x + _camera_width / 2.0) * _sprite_pix_to_world_scale
    native_pos.y = (_sprite_pix_to_world_scale * _camera_height - ((world_pos.y - _camera_position.y + _camera_height / 2.0) * _sprite_pix_to_world_scale))

    return native_pos


def world_to_screen(world_pos = Vector2()):
    '''get the screen position of a world position'''

    global _camera_position, _camera_width, _camera_height

    world_to_screen = gb.SCREEN_WIDTH / _camera_width

    screen_pos = Vector2()
    screen_pos.x = (world_pos.x - _camera_position.x + _camera_width / 2.0) * world_to_screen
    screen_pos.y = (gb.SCREEN_HEIGHT - ((world_pos.y - _camera_position.y + _camera_height / 2.0) * world_to_screen))

    return screen_pos


def screen_to_world(screen_pos = Vector2()):
    '''take a point on the screen and get it's world position'''

    global _camera_position, _camera_width, _camera_height

    world_to_screen = gb.SCREEN_WIDTH / _camera_width

    world_pos = Vector2(screen_pos.x, screen_pos.y)
    world_pos.y += gb.SCREEN_HEIGHT
    world_pos /= world_to_screen
    world_pos += _camera_position
    world_pos -= (Vector2(_camera_width, _camera_height) / 2.0)

    return world_pos



def create_game_window():
    '''create the game window'''

    gb.game_window = py.display.set_mode((gb.SCREEN_WIDTH, gb.SCREEN_HEIGHT))


def set_camera_zoom(zoom = 10.0):
    '''set the width of the camera in world units'''

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
#RECT RENDERING
#=========================================================================================================================



#rects to draw this frame
_frame_rects_to_draw = []

'''add a rect to be drawn this frame'''
def draw_rect(rect = Renderable_Rect(), pos = Vector2()):
    global _frame_rects_to_draw

    _frame_rects_to_draw.append((rect, pos))


def _render_rects():
    '''render rects to the native screen'''

    global _frame_rects_to_draw, native_render_surface, _world_to_native_pos, _sprite_pix_to_world_scale

    #draw rects to native screen
    for rect, pos in _frame_rects_to_draw:
        pos: Vector2
        rect: Renderable_Rect

        native_pos = _world_to_native_pos(pos)

        half_height = rect.height / 2.0 * _sprite_pix_to_world_scale
        top = native_pos.y + half_height
        left = native_pos.x - rect.width / 2.0 * _sprite_pix_to_world_scale

        #draw to native screen
        py.draw.rect(native_render_surface, rect.color, 
        (left, top, rect.width * _sprite_pix_to_world_scale, rect.height * _sprite_pix_to_world_scale),
        rect.border_width)

    #clear rects to draw
    _frame_rects_to_draw.clear()



#=========================================================================================================================
#TILEMAP RENDERING
#=========================================================================================================================



def _render_tilemaps():
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
    '''processor that is responsible for drawing things to the screen'''

    def process(self):
        global _world_to_native_pos, _render_sprites, _render_tilemaps, _scale_native_screen_to_window, set_native_screen, _render_rects


        set_native_screen()
        _render_tilemaps()
        _render_sprites()
        _render_rects()

        _scale_native_screen_to_window()
        py.display.flip()


class Follow_Camera_Processor(e.Processor):
    '''processor that gets the first entity w/ a follow_camera tag, and sets the camera pos to be the same as the entity's'''

    def process(self):
        global _camera_position

        camera_followers = gb.entity_world.get_components(Camera_Follow, Position)

        #if there is a camera follower then get the first one and use that
        if(len(camera_followers) > 0):
            ent, (camera_follow, pos) = camera_followers[0]
            _camera_position = pos.vector