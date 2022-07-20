from operator import truediv
import time
from core_classes import Position
import global_variables as gb
import render_manager
import input_manager
import pygame as py
import core_classes as core

py.init()

render_manager.create_game_window()

#add processors to the world
gb.entity_world.add_processor(render_manager.Render_Processor())
gb.entity_world.add_processor(render_manager.Follow_Camera_Processor())
gb.entity_world.add_processor(input_manager.Input_Processor())

#create player entity
player_entity = gb.entity_world.create_entity(
    render_manager.Renderable_Rect(), 
    core.Position(), 
    # render_manager.Camera_Follow(),
    input_manager.Input_Direction())

#main game loop
delta_time_clock = py.time.Clock()
while not gb.game_done:

    gb.delta_time = delta_time_clock.tick(60) / 1000.0

    #move player
    current_player_pos = gb.entity_world.component_for_entity(player_entity, Position)
    input_dir = gb.entity_world.component_for_entity(player_entity, input_manager.Input_Direction)
    current_player_pos.vector += input_dir.input_direction * 10.0 * gb.delta_time
        

    gb.entity_world.process()