import global_variables as gb
from dataclasses import dataclass
import pygame as py
import esper as e
import core_classes as core



#width of the camera veiw in WU (world units)
camera_zoom = 10
camera_position = core.Position()
#background color, when nothing is being rendered
background_color = (255,255,255)





def create_game_window():
    gb.game_window = py.display.set_mode((gb.SCREEN_WIDTH, gb.SCREEN_HEIGHT))




@dataclass
class Renderable_Rect:
    width, height: float
    color: py.Color

class Camera_Follow:
    def __init__(self) -> None:
        pass


class Render_Processor(e.Processor):

    def get_world_to_pix_ratio(self):
        return camera_zoom / gb.SCREEN_WIDTH

    def get_scaled_rect(self, unscaled_rect = py.Rect(0,0,0,0), world_to_pix = 0.0):
        return unscaled_rect * world_to_pix

    def get_renderables(self):
        return gb.entity_world.get_components((core.Position, Renderable_Rect))

    def get_scaled_renderables(self, world_to_pix):
        render_rects_scaled = []
    
        for ent, (render_rect, pos) in gb.entity_world.get_components(core.Position, Renderable_Rect):

            rect =  

            render_rects_scaled.append((self.get_scaled_rect(render_rect, world_to_pix), render_rect.color))

        return render_rects_scaled


    def draw_renderables(self, scaled_renderables):

        for (rect, color) in scaled_renderables:
            py.draw.rect(gb.game_window, color, rect)


    def process(self):
        
        gb.game_window.fill(background_color)

        world_to_pix = self.get_world_to_pix_ratio()

        scaled_renderables = self.get_scaled_renderables(world_to_pix)

        self.draw_renderables(scaled_renderables)

        py.display.update()