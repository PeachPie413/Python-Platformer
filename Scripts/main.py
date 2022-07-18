from operator import truediv
import time
import global_variables as gb
import render_manager
import pygame as py
import core_classes as core


render_manager.create_game_window()

gb.entity_world.add_processor(render_manager.Render_Processor())
gb.entity_world.create_entity(render_manager.Renderable_Rect(py.Rect(0,0,1,1), (100,100,100)), core.Position())

#main game loop
game_done = False
while not game_done:

    for input_event in py.event.get():
        if input_event.type == py.QUIT:
            game_done = True

    gb.entity_world.process()