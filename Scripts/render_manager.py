from core_classes import *
import global_variables as gb
from dataclasses import dataclass
import pygame as py
import esper as e
import core_classes as core
import resources
import world_data

def init():
    set_camera_zoom()
    create_game_window()

#width of the camera veiw in WU (world units)
def set_camera_zoom(zoom = 10.0):
    if zoom < 10.0: zoom = 10.0

    global _camera_width
    global _camera_height
    global camera_zoom
    global world_to_pix

    camera_zoom = zoom
    _camera_width = zoom
    _camera_height = zoom / gb.SCREEN_WIDTH_TO_HEIGHT_RATIO

    #rescale sprites
    scale_sprites()

    #reset world to pix ratio
    world_to_pix = gb.SCREEN_WIDTH / _camera_width


_camera_width = 10.0
camera_zoom = _camera_width
_camera_height = _camera_width / gb.SCREEN_WIDTH_TO_HEIGHT_RATIO
_camera_position = core.Vector2()
#background color, when nothing is being rendered
background_color = (255,255,255)
#scale for how many pixels in a sprite should be on unit long
sprite_pix_to_world_scale = 8
#scale for how many screen pixels are one unit in length for the world
world_to_pix = 0
'''func for getting pixel pos of a world pos'''
def world_to_pixel(pos = core.Vector2(), world_to_pix = 0.0):
    screen_pos = Vector2()
    screen_pos.x = (pos.x - _camera_position.x + _camera_width / 2.0) * world_to_pix
    screen_pos.y = gb.SCREEN_HEIGHT - ((pos.y - _camera_position.y + _camera_height / 2.0) * world_to_pix)
    return screen_pos

#list filled with scaled sprites, in the same order as in resources
scaled_sprites = []
def scale_sprites():

    global _camera_width

    #get factor to scale sprite resolution
    sprite_scale_factor = (gb.SCREEN_WIDTH / _camera_width) / sprite_pix_to_world_scale

    #clear list of old sprites
    scaled_sprites.clear()

    #go through sprites in resources
    for sprite in resources.sprite_list:

        #scale sprite
        ext = sprite.get_rect()[2:4]
        scaled_sprite = py.transform.scale(sprite, (int(ext[0] * sprite_scale_factor), int(ext[1] * sprite_scale_factor)))

        #add to list
        scaled_sprites.append(scaled_sprite)


def create_game_window():
    gb.game_window = py.display.set_mode((gb.SCREEN_WIDTH, gb.SCREEN_HEIGHT))




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








class Follow_Camera_Processor(e.Processor):

    def process(self):
        global _camera_position

        camera_followers = gb.entity_world.get_components(Camera_Follow, Position)

        #if there is a camera follower then get the first one and use that
        if(len(camera_followers) > 0):
            ent, (camera_follow, pos) = camera_followers[0]

            _camera_position = pos.vector










class Render_Processor(e.Processor):

    def get_world_to_pix_ratio(self):
        global _camera_width
        return gb.SCREEN_WIDTH / _camera_width

    def get_scaled_rect(self, unscaled_rect = Renderable_Rect(), world_to_pix = 0.0, pos = core.Position()):

        global _camera_position
        global _camera_height
        global _camera_width

        screen_pos = world_to_pixel(Vector2(pos.vector.x - unscaled_rect.width / 2.0, pos.vector.y + unscaled_rect.height / 2.0), world_to_pix)

        return py.Rect(
            screen_pos.x, screen_pos.y,
            unscaled_rect.width * world_to_pix, unscaled_rect.height * world_to_pix
        )

    def get_scaled_rects(self, world_to_pix):
        render_rects_scaled = []
    
        for ent, (pos, render_rect) in gb.entity_world.get_components(core.Position, Renderable_Rect):
            render_rects_scaled.append((self.get_scaled_rect(render_rect, world_to_pix, pos), render_rect.color))

        return render_rects_scaled

    def draw_rects(self, scaled_renderables):

        for (rect, color) in scaled_renderables:
            py.draw.rect(gb.game_window, color, rect)

    def render_rects(self, world_to_pix = 0.0):
        scaled_rects = self.get_scaled_rects(world_to_pix)

        self.draw_rects(scaled_rects)





    #SPRITE RENDERING
    def get_sprites(self):
        sprites = []

        for ent, (pos, sprite) in gb.entity_world.get_components(core.Position, Sprite):

            sprites.append((pos.vector, sprite.sprite_id))

        return sprites


    '''take the sprites' world pos and turn it into a screen pos'''
    def scale_sprites(self, sprites, world_to_pix):
        
        global sprite_pix_to_world_scale

        index = 0
        for (pos, sprite_id) in sprites:

            sprite_metadata = resources.sprite_metadata_list[sprite_id]
            scaled_pos = world_to_pixel(Vector2(pos.x - sprite_metadata.size.x / 2.0 / sprite_pix_to_world_scale, pos.y + sprite_metadata.size.y / 2.0 / sprite_pix_to_world_scale), world_to_pix)

            sprites[index] = (scaled_pos, sprite_id)

            index += 1

        return sprites


    '''draw the scaled sprites to the screen'''
    def draw_sprites(self, sprites):
        
        global scaled_sprites

        for (pos, sprite_id) in sprites:

            gb.game_window.blit(scaled_sprites[sprite_id], (pos.x, pos.y))


    def render_sprites(self, world_to_pix):
        sprites = self.get_sprites()

        sprites = self.scale_sprites(sprites, world_to_pix)

        self.draw_sprites(sprites)






    #render tilemaps
    def render_chunks(self):
        
        chunks = self.get_chunks()

        scaled_tiles = self.scale_tilemaps(chunks)

        self.draw_tilemaps(scaled_tiles)


    def get_chunks(self):
        global _camera_position

        #get chunks in the camera veiw
        camera_chunk_pos = world_data.world_pos_to_chunk(_camera_position)
        chunk_positions = []
        for x in range(camera_chunk_pos.x - 1, camera_chunk_pos.x +2):
            for y in range(camera_chunk_pos.y - 1, camera_chunk_pos.y +2):
                chunk_positions.append(Vector2(x,y))

        #get chunks
        chunks = []
        for chunk_pos in chunk_positions:
            chunk = world_data.get_chunk_from_chunk_pos(chunk_pos)

            if chunk is not None:
                chunks.append(chunk)

        return chunks



    def scale_tilemaps(self, unscaled_chunks):
        pass


    def draw_tilemaps(self, chunks):
        global world_to_pix

        for chunk in chunks:
            






    def process(self):

        gb.game_window.fill(background_color)

        world_to_pix = self.get_world_to_pix_ratio()

        self.render_rects(world_to_pix)

        self.render_chunks()

        self.render_sprites(world_to_pix)

        py.display.update()