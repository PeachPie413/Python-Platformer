from core_classes import *
import esper as e
import input_manager
import physics
import global_variables as gb


#define global player stuff
MAX_PLAYER_SPEED = 100.0
PLAYER_ACCELERATION = 1.0
PLAYER_JUMP_FORCE = 1.0
PLAYER_GROUND_FRICTION = 10.0
PLAYER_AIR_FRICTION = 1.0



class Character_Controller_Processor(e.Processor):

    def process(self):

        global MAX_PLAYER_SPEED
        global PLAYER_ACCELERATION
        global PLAYER_JUMP_FORCE
        global PLAYER_GROUND_FRICTION
        global PLAYER_AIR_FRICTION

        #go through all players
        for ent, (veloc, collided, move_dir) in gb.entity_world.get_components(physics.Velocity, physics.Collided_Prev_Frame, input_manager.Input_Direction):

            move_imp_force = Vector2()

            #check if player wants to move left or right, and is under the max speed
            if not move_dir.input_direction.x == 0 and abs(veloc.vector.x) < MAX_PLAYER_SPEED:

                #add impulse of left or right movement to movement impulse force
                move_imp_force.x += move_dir.input_direction.x * PLAYER_ACCELERATION

            #if there is force to add to the player, then add it
            gb.entity_world.add_component(ent, physics.Impulse_Force(move_imp_force))