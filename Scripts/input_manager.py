from turtle import down
import core_classes as core
import pygame as py
import esper as e
import global_variables as gb

#for input store keys for things in global variables here, then have
#different components for different things, ex a direction input gives
#a vec2 for the player input dir, regardless of keys or hardware
#things then use this dir to do stuff


up_key = py.K_w
down_key = py.K_s
right_key = py.K_d
left_key = py.K_a

#input datas
input_dir = core.Vector2()
scroll_delta = 0.0


class Input_Direction():

    def __init__(self, input_dir = core.Vector2()) -> None:
        self.input_direction = input_dir


class Scroll_Amount():
    def __init__(self) -> None:
        self.delta = 0.0



class Input_Direction_Processor(e.Processor):

    def set_input_variables(self):

        global up_key
        global down_key
        global left_key
        global right_key

        global input_dir
        global scroll_delta

        scroll_delta = 0
        for input_event in py.event.get():

            if input_event.type == py.QUIT:
                gb.game_done = True

            if input_event.type == py.MOUSEWHEEL:
                scroll_delta = input_event.y
            else:
                scroll_delta = 0

        #key press stuff
        keys = py.key.get_pressed()
        if keys[up_key]:
            input_dir.y = 1
        elif keys[down_key]:
            input_dir.y = -1
        else:
            input_dir.y = 0
        if keys[left_key]:
            input_dir.x = -1
        elif keys[right_key]:
            input_dir.x = 1
        else:
            input_dir.x = 0

        #normailize input dir
        if abs(input_dir.x) == 1.0 and abs(input_dir.y) == 1.0:
            input_dir *= 0.7 




    def set_input_dir(self):

        global input_dir

        for ent, input_dir_component in gb.entity_world.get_component(Input_Direction):
            input_dir_component.input_direction = input_dir


    def set_scroll_delta(self):

        global scroll_delta

        for ent, scroll in gb.entity_world.get_component(Scroll_Amount):
            scroll.delta = scroll_delta


    def process(self):

        input_dir = core.Vector2()

        self.set_input_variables()

        self.set_input_dir()

