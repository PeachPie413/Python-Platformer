import pygame as py
import global_variables as gb
import esper as e
from core_classes import *
import math



class Velocity():
    def __init__(self, vector = Vector2()):
        self.vector = vector

class Collider:
    def __init__(self, width = 0, height = 0):
        self.width = width
        self.height = height

class Constant_Force:
    def __init__(self, forces = []) -> None:
        self.forces = forces
        self.reaction_forces = Vector2()

class Impulse_Force:
    def __init__(self, vector = Vector2()) -> None:
        self.vector = vector

class Mass:
    def __init__(self, mass = 1.0) -> None:
        self.mass = mass

class Collided_Prev_Frame:
    def __init__(self) -> None:
        self.collided = False
        self.collision_side = Vector2()

class Friction:
    def __init__(self, ground_mu = 0.0, air_mu = 0.0) -> None:
        self.ground_mu = ground_mu
        self.air_mu = air_mu
        



class Forces_Processor(e.Processor):

    def process(self):
        
        for ent, (mass, force, veloc) in gb.entity_world.get_components(Mass, Constant_Force, Velocity):
            #get sum of forces on object
            force_sum = Vector2()
            for vec in force.forces:
                force_sum += vec
            force_sum += force.reaction_forces
            
            #multiply by delta time
            force_sum *= gb.delta_time

            #see if it has a impulse force component
            impulse = gb.entity_world.try_component(ent, Impulse_Force)
            if impulse != None:
                #if it has a impulse component then add it's force and remove it from the entity
                force_sum += impulse.vector
                gb.entity_world.remove_component(ent, Impulse_Force)

            #change veloc based on forces and mass
            veloc.vector += force_sum / mass.mass


class Velocity_Processor(e.Processor):


    '''check if 2 aabb's are colliding'''
    def aabb_collision(self, a_collider = Collider(), a_pos = Position(), b_collider = Collider(), b_pos = Position()):
        a_max_x = a_pos.vector.x + a_collider.width / 2.0
        a_min_x = a_pos.vector.x - a_collider.width / 2.0
        b_max_x = b_pos.vector.x + b_collider.width / 2.0
        b_min_x = b_pos.vector.x - b_collider.width / 2.0
        a_max_y = a_pos.vector.y + a_collider.height / 2.0
        a_min_y = a_pos.vector.y - a_collider.height / 2.0
        b_max_y = b_pos.vector.y + b_collider.height / 2.0
        b_min_y = b_pos.vector.y - b_collider.height / 2.0
        return a_max_x >= b_min_x and b_max_x >= a_min_x and a_max_y >= b_min_y and b_max_y >= a_min_y


    '''returns the collider it is colliding with'''
    def collider_is_colliding(self, self_pos = Position(), self_collider = Collider(), self_ent = 0):

        #go through all possible things to collide wit
        for ent, (pos, collider) in gb.entity_world.get_components(Position, Collider):

            #skip if the collider is the colliding one
            if(ent == self_ent): continue

            #check if they are colliding
            if(self.aabb_collision(collider, pos, self_collider, self_pos)):
                return (collider, pos)

        return None
            

    '''set pos of collider given the collider it colides with. Returns side it collided with using a vec2'''
    def set_post_collision_pos(self, pos = Vector2(), collider = Collider(), colliding_collider = Collider(), colliding_pos = Vector2()):

        #get move amount for dimensions
        move_amount_x = (collider.width + colliding_collider.width) / 2.0 - abs(pos.x - colliding_pos.x)
        move_amount_y = (collider.height + colliding_collider.height) / 2.0 - abs(pos.y - colliding_pos.y)

        #collision moving into vertical surface
        if move_amount_x < move_amount_y:

            #get amount to move on x axis
            delta_pos = math.copysign(move_amount_x, pos.x - colliding_pos.x)
            pos.x += delta_pos
            
            #return collision side
            return Vector2(math.copysign(1, delta_pos), 0)

        #collision moving into horizontal surface
        else:
            #get amount to move on y axis
            delta_pos = math.copysign(move_amount_y, pos.y - colliding_pos.y)
            pos.y += delta_pos

            #return collision side
            return Vector2(0, math.copysign(1, delta_pos))


    '''set the forces on an object to equal 0 on the y axis when it is colliding with the ground'''
    def cancel_const_forces(self, forces = Constant_Force()):
        #get sum of forces
        force_sum = 0.0
        for force in forces.forces:
            force_sum += force.y
        
        #if sum of forces not 0, then add a force that equals 0
        if force_sum != 0.0:
            forces.reaction_forces = Vector2(0, -force_sum)


    '''apply friction to an object on the horizontal axis'''
    def apply_friction(self, veloc, mu):
        veloc.x -= mu * veloc.x * gb.delta_time



    def process(self):

        #go through all entities w/ pos, veloc, and collider
        for ent, (pos, veloc, collider, forces, collided, friction) in gb.entity_world.get_components(Position, Velocity, Collider, Constant_Force, Collided_Prev_Frame, Friction):

            #skip if velocity is 0
            if(veloc.vector == Vector2()): continue

            #set new position
            pos.vector += veloc.vector * gb.delta_time

            #check if there is a colliding collider
            if (colliding_collider_data := self.collider_is_colliding(pos, collider, ent)) != None:

                #set pos and get side it collides with
                collide_side = self.set_post_collision_pos(pos.vector, collider, colliding_collider_data[0], colliding_collider_data[1].vector)

                #apply friction, if collision on x axis
                if collide_side.y == 1 or collide_side.y == -1:
                    self.apply_friction(veloc.vector, friction.ground_mu)

                #create cancel force and set veloc to 0 if wasnt colliding last frame and collided with floor
                if not collided.collision_side == Vector2():
                    if collide_side.y == 1:
                        self.cancel_const_forces(forces)

                    
                    if collide_side:
                        veloc.vector.y = 0
                    else:
                        veloc.vector.x = 0

                #set collided last frame
                collided.collision_side = collide_side

            #else did not collide this frame
            else:
                
                #apply friction
                self.apply_friction(veloc.vector, friction.air_mu)

                #if collided last frame then remove ground force
                if collided.collision_side != Vector2():
                    forces.reaction_forces = Vector2()

                #say no longer collided
                collided.collision_side = Vector2()