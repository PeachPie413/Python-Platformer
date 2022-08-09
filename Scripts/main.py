from core_classes import *
from input_manager import Input_Direction
from rendering.rendering import Camera_Follow
from core_classes import Vector2
from core_classes import Position
import global_variables as gb
import rendering.rendering as render_manager
import input_manager
import physics.physics as physics
import pygame as py
import core_classes as core
import character_controller
import resources.resources as resources
import world_data.world_data as world_data
import esper as e
import chunk_colliders.chunk_colliders as chunk_colliders

py.init()

resources.load_assets()
render_manager.init()

tile = world_data.Tile(resources.tile_type_dict['stone'])
chunk = world_data.create_chunk()
chunk.tile_data = Grid(world_data.CHUNK_SIZE, world_data.CHUNK_SIZE, tile)

#add processors to the world
#rendering
gb.entity_world.add_processor(render_manager.Render_Processor(), -99)
gb.entity_world.add_processor(render_manager.Follow_Camera_Processor(), -98)
#input
gb.entity_world.add_processor(input_manager.Input_Direction_Processor(), 89)
#player movement
gb.entity_world.add_processor(character_controller.Character_Controller_Processor())
#physics
gb.entity_world.add_processor(physics.Forces_Processor(), 98)
gb.entity_world.add_processor(physics.Velocity_Processor(), 99)

#create player entity
# player = gb.entity_world.create_entity(
#     Position(Vector2(0,3)),
#     Collider(1,1),
#     render_manager.Sprite(0),
#     Velocity(),
#     input_manager.Input_Direction(),
#     render_manager.Camera_Follow(),
#     physics.Constant_Force([Vector2(0,-9.8)]),
#     physics.Mass(),
#     physics.Collided_Prev_Frame(),
#     physics.Friction(character_controller.PLAYER_GROUND_FRICTION, character_controller.PLAYER_AIR_FRICTION),
#     input_manager.Scroll_Amount()
# )

#camera that moves w/ keyboard input
camera = gb.entity_world.create_entity(
    input_manager.Input_Direction(),
    render_manager.Camera_Follow(),

    Position()
)

chunk_colliders.create_colliders()

#main game loop
delta_time_clock = py.time.Clock()
while not gb.game_done:

    gb.delta_time = delta_time_clock.tick(60) / 1000.0

    if input_manager.scroll_delta != 0:
        render_manager.set_camera_zoom(render_manager.camera_zoom + input_manager.scroll_delta)

    if input_manager.input_dir.as_tuple() != (0.0, 0.0):
        for ent, (pos, input_dir) in gb.entity_world.get_components(Position, input_manager.Input_Direction):
            pos.vector += Vector2(input_manager.input_dir.x * gb.delta_time * 10, input_manager.input_dir.y * gb.delta_time * 10)

    physics.Render_Colliders()

    #print mouse pos to console
    # mouse_pos = py.mouse.get_pos()
    # print(render_manager.screen_to_world(Vector2(mouse_pos[0], mouse_pos[1])).as_tuple())

    gb.entity_world.process()