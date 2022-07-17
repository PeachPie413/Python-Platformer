import global_variables as gb
from dataclasses import dataclass
import pygame as py
import esper as e
import core_classes as core




camera_zoom = 0.0
camera_position = core.Position()





def create_game_window():
    gb.game_window = py.display.set_mode((gb.SCREEN_WIDTH, gb.SCREEN_HEIGHT))




@dataclass
class Renderable_Rect:
    rect: py.Rect
    color: py.Color




class Render_Processor(e.Processor):

    def get_renderables(self):
        pass

    def scale_renderables_to_screen(self, renderables):
        pass

    def draw_renderables(self, scaled_renderables):
        pass


    def process(self):
        
        renderables = self.get_renderables()

        scaled_renderables = self.scale_renderables_to_screen(renderables)

        self.draw_renderables(scaled_renderables)