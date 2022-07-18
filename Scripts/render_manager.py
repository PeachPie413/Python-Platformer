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




class Renderable_Rect:
    def __init__(self, color = (255, 192, 203), width = 1.0, height = 1.0) -> None:
        self.color = color
        self.width = width
        self.height = height

class Camera_Follow:
    def __init__(self) -> None:
        pass


class Render_Processor(e.Processor):

    def get_world_to_pix_ratio(self):
        return gb.SCREEN_WIDTH / camera_zoom

    def get_scaled_rect(self, unscaled_rect = Renderable_Rect(), world_to_pix = 0.0, pos = core.Position()):

        left = float(pos.x - unscaled_rect.width / 2.0) * world_to_pix
        top = float(pos.y + unscaled_rect.height / 2.0) * world_to_pix

        return py.Rect(
            left, top,
            unscaled_rect.width * world_to_pix, unscaled_rect.height * world_to_pix
        )

    def get_renderables(self):
        return gb.entity_world.get_components((core.Position, Renderable_Rect))

    def get_scaled_renderables(self, world_to_pix):
        render_rects_scaled = []
    
        for ent, (pos, render_rect) in gb.entity_world.get_components(core.Position, Renderable_Rect):
            render_rects_scaled.append((self.get_scaled_rect(render_rect, world_to_pix, pos), render_rect.color))

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