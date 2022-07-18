from operator import truediv
import time
from core_classes import Position
import global_variables as gb
import render_manager
import pygame as py
import core_classes as core


render_manager.create_game_window()

gb.entity_world.add_processor(render_manager.Render_Processor())
player_entity = gb.entity_world.create_entity(render_manager.Renderable_Rect(), core.Position())

#main game loop
game_done = False
while not game_done:

    for input_event in py.event.get():
        if input_event.type == py.QUIT:
            game_done = True

        #move player
        current_player_pos = gb.entity_world.component_for_entity(player_entity, Position)
        if input_event.type == py.K_d:
            current_player_pos.x += 1
        if input_event.type == py.K_a:
            current_player_pos.x -= 1
        if input_event.type == py.K_w:
            current_player_pos.y += 1
        if input_event.type == py.K_s:
            current_player_pos.y -= 1
        

    gb.entity_world.process()