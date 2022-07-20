import pygame as py
import esper as e

game_window = py.surface.Surface((0,0))
entity_world = e.World()
delta_time = 0.0
game_done = False

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 300
SCREEN_WIDTH_TO_HEIGHT_RATIO = SCREEN_WIDTH / SCREEN_HEIGHT