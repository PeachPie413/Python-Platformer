from core_classes import *
import helper_funcs
from input_manager import Input_Direction
from rendering.rendering import Camera_Follow
from core_classes import Vector2
from core_classes import Position
import global_variables as gb
import rendering.rendering as render_manager
import input_manager
import physics.physics as physics
import physics.globals as physics_globals
import pygame as py
import character_controller
import resources.resources as resources
import resources.globals as resources_globals
import world_data.world_data as world_data
import world_data.click_change_tile as click_change_tile
import esper as e
import chunk_colliders.chunk_colliders as chunk_colliders

py.init()

resources.load_assets()
render_manager.init()
chunk_colliders.init()

#world_data.create_chunks_in_square()

# collider = gb.entity_world.create_entity(Position())
# physics.register_collider(collider, is_dynamic=False)
mouse_collider = gb.entity_world.create_entity(Position(render_manager.get_mouse_world_pos()))
physics.register_collider(mouse_collider)

print(Vector2(0.0, 0.0).to_tuple() != Vector2(-1, 0).to_tuple())

#add processors to the world
#rendering
gb.entity_world.add_processor(render_manager.Render_Processor(), -99)
gb.entity_world.add_processor(render_manager.Follow_Camera_Processor(), -98)
#input
gb.entity_world.add_processor(input_manager.Input_Direction_Processor(), 89)
#player movement
gb.entity_world.add_processor(character_controller.Character_Controller_Processor())
#physics
#gb.entity_world.add_processor(physics.Forces_Processor(), 98)
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

#main game loop
delta_time_clock = py.time.Clock()
while not gb.game_done:

    gb.delta_time = delta_time_clock.tick(60) / 1000.0

    if input_manager.scroll_delta != 0:
        render_manager.set_camera_zoom(render_manager.camera_zoom + input_manager.scroll_delta)

    if input_manager.input_dir.to_tuple() != (0.0, 0.0):
        for ent, (pos, input_dir) in gb.entity_world.get_components(Position, input_manager.Input_Direction):
            pos.vector += Vector2(input_manager.input_dir.x * gb.delta_time * 10, input_manager.input_dir.y * gb.delta_time * 10)

    if physics_globals.DEBUG_RENDER_COLLIDERS:
        physics.Render_Colliders()

    if world_data.DEBUG_SHOW_CHUNK_BORDERS:
        world_data.show_chunk_borders()

    if physics_globals.DEBUG_RENDER_BUCKETS:
        physics.render_buckets()

    #if input_manager.left_click_pressed:
        #click_change_tile._place_tile_at_mouse_pos('stone')

    if input_manager.left_click and input_manager.mouse_button_down:
        collider = gb.entity_world.create_entity(Position(render_manager.get_mouse_world_pos()))
        physics.register_collider(collider)

    if input_manager.right_click:
        click_change_tile._place_tile_at_mouse_pos(None)

    pos = gb.entity_world.component_for_entity(mouse_collider, Position)
    pos.vector = render_manager.get_mouse_world_pos()

    gb.entity_world.process()