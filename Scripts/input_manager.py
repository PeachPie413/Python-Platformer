import core_classes as core
import pygame as py

#for input store keys for things in global variables here, then have
#different components for different things, ex a direction input gives
#a vec2 for the player input dir, regardless of keys or hardware
#things then use this dir to do stuff


up_key = py.K_w
down_key = py.K_s
right_key = py.K_a
left_key = py.K_d


class Input_Move_Direction():

    def __init__(self) -> None:
        self.