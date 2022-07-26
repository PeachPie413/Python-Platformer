from turtle import position
from input_manager import Input_Direction
from render_manager import Camera_Follow
from core_classes import Vector2
from physics import Collider, Velocity
from core_classes import Position
import global_variables as gb
import render_manager
import input_manager
import physics
import pygame as py
import core_classes as core

py.init()

render_manager.create_game_window()

#add processors to the world
gb.entity_world.add_processor(render_manager.Render_Processor(), -99)
gb.entity_world.add_processor(render_manager.Follow_Camera_Processor())
gb.entity_world.add_processor(input_manager.Input_Processor())
gb.entity_world.add_processor(physics.Forces_Processor(), 98)
gb.entity_world.add_processor(physics.Velocity_Processor(), 99)

#create player entity
falling_box = gb.entity_world.create_entity(
    Position(Vector2(0,3)),
    Collider(1,1),
    render_manager.Renderable_Rect(),
    Velocity(),
    input_manager.Input_Direction(),
    render_manager.Camera_Follow(),
    physics.Constant_Force([Vector2(0,-2)]),
    physics.Mass(),
    physics.Collided_Prev_Frame()
)
platform = gb.entity_world.create_entity(
    Position(Vector2(0,-3)),
    Collider(6,1),
    render_manager.Renderable_Rect((0,0,0), 6, 1)
)
# camera = gb.entity_world.create_entity(
#     input_manager.Input_Direction(),
#     render_manager.Camera_Follow(),
#     Position()
# )

#main game loop
delta_time_clock = py.time.Clock()
while not gb.game_done:

    gb.delta_time = delta_time_clock.tick(60) / 1000.0

    pos = gb.entity_world.component_for_entity(falling_box, Position)
    input_dir = gb.entity_world.component_for_entity(falling_box, Input_Direction)
    if input_dir.input_direction.x == 1:
        pos.vector.y = 3

    gb.entity_world.process()