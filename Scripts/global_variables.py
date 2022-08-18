import pygame as py
import esper as e

game_window = py.surface.Surface((0,0))
entity_world = e.World()
delta_time = 0.0
game_done = False
gravity_acceleration = 9.82

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_WIDTH_TO_HEIGHT_RATIO = SCREEN_WIDTH / SCREEN_HEIGHT