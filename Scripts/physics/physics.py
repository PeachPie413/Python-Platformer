import pygame as py
import global_variables as gb
import esper as e
from core_classes import *
import math
from physics.globals import *
import rendering.rendering as rendering
import helper_funcs



class Velocity():
    def __init__(self, vector = Vector2()):
        self.vector = vector

class Shape:
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

class CollisionState:
    def __init__(self, collision_state = Vector2()) -> None:
        self.collision_state = collision_state

class Friction:
    def __init__(self, ground_mu = 0.0, air_mu = 0.0) -> None:
        self.ground_mu = ground_mu
        self.air_mu = air_mu
        

_bucket_size = 10
'''length of a side of each bucket'''
_bucket_radius = 1
'''radius around each bucket to return when asked for colliders, cant be lower than 1'''
class PhysicsWorld:
    '''data type that stores all colliders'''

    def __init__(self) -> None:
        self.buckets = {}

    def get_nearby_colliders(self, world_pos = Vector2()):
        global _bucket_size, _bucket_radius
        
        colliders = []

        #get buckets to check for
        bucket_pos = self.get_bucket_pos(world_pos)
        bucket_positions = helper_funcs.get_positions_in_square(_bucket_radius, bucket_pos)

        #for each bucket to check
        for pos in bucket_positions:

            #if in bucket dict, append to colliders
            if pos.to_tuple() in self.buckets:
                colliders.extend(self.buckets[pos.to_tuple()])

        return colliders


    def get_bucket_pos(self, world_pos = Vector2()):
        return Vector2(floor(world_pos.x / _bucket_size), floor(world_pos.y / _bucket_size))

    
    def add_collider(self, world_pos = Vector2(), collider_entity = int):
        '''add a collider to the physics world'''

        bucket_pos = self.get_bucket_pos(world_pos).to_tuple()
        bucket = None

        #get bucket
        if bucket_pos not in self.buckets:
            bucket = []
            self.buckets[bucket_pos] = bucket
        else:
            bucket = self.buckets[bucket_pos]

        bucket.append(collider_entity)




#=========================================================================================================================
#MANAGING COLLDIERS
#=========================================================================================================================



_physics_world = PhysicsWorld()

def register_collider(entity = int, width = 1, height = 1, is_dynamic = True, mass = 1):
    '''add a collider to the physics world, and attach all needed components to it, requires a position already'''
    global _physics_world

    #add components
    shape = Shape(width, height)
    gb.entity_world.add_component(entity, shape)
    #add components needed for dynamic collider
    if is_dynamic:
        velocity = Velocity()
        gb.entity_world.add_component(entity, velocity)
        mass = Mass(mass)
        gb.entity_world.add_component(entity, mass)
        constant_force = Constant_Force()
        gb.entity_world.add_component(entity, constant_force)
        collision_state = CollisionState()
        gb.entity_world.add_component(entity, collision_state)

    #add collider to physics world
    _physics_world.add_collider(gb.entity_world.component_for_entity(entity, Position).vector, entity)

    


#=========================================================================================================================
#DEBUGGING
#=========================================================================================================================



def Render_Colliders():
    global DEBUG_RENDER_COLLIDERS, DEBUG_COLLIDER_COLOR

    #go through all enttiies w/ a pos and a collider and render them
    for ent, (pos, collider) in gb.entity_world.get_components(Position, Shape):
        pos: Position
        collider: Shape

        rendering.draw_rect(
            rendering.Renderable_Rect(DEBUG_COLLIDER_COLOR, collider.width, collider.height, 2),
            pos.vector
        )



#=========================================================================================================================
#NORMALS
#=========================================================================================================================


def _calculate_normals(collision_state = Vector2(), const_forces = {}, velocity = Vector2()):
    '''calculate and set the normal forces for a collider and set it's veloc to be 0 where collided'''

    #cancel out velocity
    _veloc_to_zero(velocity.x)
    _veloc_to_zero(velocity.y)

    #set normal forces
    _set_normal_forces(const_forces, collision_state)


def _veloc_to_zero(veloc = 0.0):
    '''if there is a velocity then set it to 0'''

    if veloc != 0:
        veloc = 0.0


_normal_x_name = 'normal x'
_normal_y_name = 'normal y'
def _set_normal_forces(const_forces = {}, collision_state = Vector2()):
    '''set the normal force for an axis'''
    global _normal_x_name, _normal_y_name

    #get sum of forces
    force_sum = Vector2()
    for force_name in const_forces.keys():

        if force_name is _normal_x_name or force_name is _normal_y_name:
            continue

        force_sum += const_forces[force_name]
    

    #if no collision then remove force from dict, if it's in there
    if collision_state.x is 0.0:

        if _normal_x_name in const_forces:
            del const_forces[_normal_x_name]

    if collision_state.y is 0.0:

        if _normal_y_name in const_forces:
            del const_forces[_normal_y_name]


    #depending on collision state, add normal forces
    if collision_state.x is not 0.0:
        const_forces[_normal_x_name] = Vector2(-force_sum.x, 0)

    if collision_state.y is not 0.0:
        const_forces[_normal_y_name] = Vector2(0, -force_sum.y)



#=========================================================================================================================
#VELOCITY 
#=========================================================================================================================



def calculate_positions(velocity):
    '''calcuate the new position of all dynamic colliders'''



#=========================================================================================================================
#PROCESSORS
#=========================================================================================================================



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


    def aabb_collision(self, a_collider = Shape(), a_pos = Position(), b_collider = Shape(), b_pos = Position()):
        '''check if 2 aabb's are colliding'''
        a_max_x = a_pos.vector.x + a_collider.width / 2.0
        a_min_x = a_pos.vector.x - a_collider.width / 2.0
        b_max_x = b_pos.vector.x + b_collider.width / 2.0
        b_min_x = b_pos.vector.x - b_collider.width / 2.0
        a_max_y = a_pos.vector.y + a_collider.height / 2.0
        a_min_y = a_pos.vector.y - a_collider.height / 2.0
        b_max_y = b_pos.vector.y + b_collider.height / 2.0
        b_min_y = b_pos.vector.y - b_collider.height / 2.0
        return a_max_x >= b_min_x and b_max_x >= a_min_x and a_max_y >= b_min_y and b_max_y >= a_min_y


    def collider_is_colliding(self, self_pos = Position(), self_collider = Shape(), self_ent = 0):
        '''returns the collider it is colliding with'''

        #go through all possible things to collide wit
        for ent, (pos, collider) in gb.entity_world.get_components(Position, Shape):

            #skip if the collider is the colliding one
            if(ent == self_ent): continue

            #check if they are colliding
            if(self.aabb_collision(collider, pos, self_collider, self_pos)):
                return (collider, pos)

        return None
            

    def set_post_collision_pos(self, pos = Vector2(), collider = Shape(), colliding_collider = Shape(), colliding_pos = Vector2()):
        '''set pos of collider given the collider it colides with. Returns side it collided with using a vec2'''

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
        '''do physics calculations'''
        global _calculate_normals

        # #go through all entities w/ pos, veloc, and collider
        # for ent, (pos, veloc, collider, forces, collided, friction) in gb.entity_world.get_components(Position, Velocity, Collider, Constant_Force, Collided_Prev_Frame, Friction):

        #     #skip if velocity is 0
        #     if(veloc.vector == Vector2()): continue

        #     #set new position
        #     pos.vector += veloc.vector * gb.delta_time

        #     #check if there is a colliding collider
        #     if (colliding_collider_data := self.collider_is_colliding(pos, collider, ent)) != None:

        #         #set pos and get side it collides with
        #         collide_side = self.set_post_collision_pos(pos.vector, collider, colliding_collider_data[0], colliding_collider_data[1].vector)

        #         #apply friction, if collision on x axis
        #         if collide_side.y == 1 or collide_side.y == -1:
        #             self.apply_friction(veloc.vector, friction.ground_mu)

        #         #create cancel force and set veloc to 0 if wasnt colliding last frame and collided with floor
        #         if not collided.collision_side == Vector2():
        #             if collide_side.y == 1:
        #                 self.cancel_const_forces(forces)

                    
        #             if collide_side:
        #                 veloc.vector.y = 0
        #             else:
        #                 veloc.vector.x = 0

        #         #set collided last frame
        #         collided.collision_side = collide_side

        #     #else did not collide this frame
        #     else:
                
        #         #apply friction
        #         self.apply_friction(veloc.vector, friction.air_mu)

        #         #if collided last frame then remove ground force
        #         if collided.collision_side != Vector2():
        #             forces.reaction_forces = Vector2()

        #         #say no longer collided
        #         collided.collision_side = Vector2()