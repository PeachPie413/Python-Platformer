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

class CurrentBucketPos:
    def __init__(self, pos = Vector2()) -> None:
        self.vector = pos
        

_bucket_size = 10.0
'''length of a side of each bucket'''
_bucket_radius = 1.0
'''radius around each bucket to return when asked for colliders, cant be lower than 1'''
class PhysicsWorld:
    '''data type that stores all colliders'''

    def __init__(self) -> None:
        self.buckets = {}

    def get_nearby_colliders(self, world_pos = Vector2()):
        '''get the colliders nearby a position. collider is list of entity IDs. Will return the collider with the world pos given'''
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

    
    def add_collider(self, collider_entity = 0):
        '''add a collider to the physics world'''

        world_pos = gb.entity_world.component_for_entity(collider_entity, Position).vector
        bucket_pos = self.get_bucket_pos(world_pos)

        #get bucket
        bucket = self._get_bucket(bucket_pos)

        bucket.append(collider_entity)


    def update_collider_pos(self, old_bucket_pos = Vector2(), new_pos = Vector2(), entity = 0):
        '''see if a colldier needs to be changed to a new bucket, and if so then update it'''

        #check if bucket has changed
        new_bucket_pos = _physics_world.get_bucket_pos(new_pos)
        if new_bucket_pos.to_tuple() != old_bucket_pos.to_tuple():

            #if old bucket does exist
            if old_bucket_pos.to_tuple() in self.buckets:

                #then remove from old bucket
                old_bucket = self._get_bucket(old_bucket_pos)
                if entity in old_bucket:
                    old_bucket.remove(entity)

                #try remove it
                self._try_remove_bucket(old_bucket_pos)

            #add to new bucket
            new_bucket = self._get_bucket(new_bucket_pos)
            new_bucket.append(entity)

        #return new bucket pos
        return new_bucket_pos


    def _try_remove_bucket(self, bucket_pos = Vector2()):
        '''remove a bucket from buckets if it is empty'''
        bucket_key = bucket_pos.to_tuple()

        bucket = self.buckets[bucket_key]

        if len(bucket) == 0:
            del self.buckets[bucket_key]


    def _get_bucket(self, bucket_pos = Vector2()):
        '''get a bucket at the bucket pos, creates a new bucket if one does not exist'''

        bucket = None
        bucket_key = bucket_pos.to_tuple()

        if bucket_key not in self.buckets:
            bucket = []
            self.buckets[bucket_key] = bucket
        else:
            bucket = self.buckets[bucket_key]

        return bucket
            



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
        prev_pos = CurrentBucketPos()
        gb.entity_world.add_component(entity, prev_pos)

    #add collider to physics world
    _physics_world.add_collider(entity)

    


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


def render_buckets():
    '''render the buckets of the physics world'''
    global _physics_world, _bucket_size, DEBUG_BUCKET_COLOR

    for bucket_pos in _physics_world.buckets:

        center = Vector2(bucket_pos[0] * _bucket_size + _bucket_size / 2, bucket_pos[1] * _bucket_size + _bucket_size / 2)

        rendering.draw_rect(
            rendering.Renderable_Rect(DEBUG_BUCKET_COLOR, _bucket_size, _bucket_size, 1),
            center
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



def _calculate_positions():
    '''calcuate the new position of all dynamic colliders'''
    global _pos_valid, _physics_world

    #go through all dynamic colliders
    for ent, (pos, velocity, shape, collision_state, current_bucket_pos) in gb.entity_world.get_components(Position, Velocity, Shape, CollisionState, CurrentBucketPos):

        #skip if velocity is 0
        # if velocity.vector == Vector2():
        #     continue

        #get new position using velocity
        new_pos = pos.vector + velocity.vector * gb.delta_time

        #change physics world bucket if needed, and update bucket pos        
        current_bucket_pos.vector = _physics_world.update_collider_pos(current_bucket_pos.vector, new_pos, ent)

        #do collision check
        collided_data = _pos_valid(new_pos, shape, pos.vector, ent)

        #check if new position is valid
        if collided_data != None:
            
            #if not then calculate new pos
            new_pos = _get_collided_pos(pos, shape, collided_data[0], collided_data[1])

        #set collision state

        #set new pos
        pos.vector = new_pos


def _aabb_collision(a_collider = Shape(), a_pos = Vector2(), b_collider = Shape(), b_pos = Vector2()):
    '''check if 2 aabb's are colliding'''
    a_max_x = a_pos.x + a_collider.width / 2.0
    a_min_x = a_pos.x - a_collider.width / 2.0
    b_max_x = b_pos.x + b_collider.width / 2.0
    b_min_x = b_pos.x - b_collider.width / 2.0
    a_max_y = a_pos.y + a_collider.height / 2.0
    a_min_y = a_pos.y - a_collider.height / 2.0
    b_max_y = b_pos.y + b_collider.height / 2.0
    b_min_y = b_pos.y - b_collider.height / 2.0
    return a_max_x >= b_min_x and b_max_x >= a_min_x and a_max_y >= b_min_y and b_max_y >= a_min_y


def _pos_valid(pos = Vector2(), shape = Shape(), old_pos = Vector2(), entity = 0):
    '''check if a position and shape is not colliding with any other collider, returns collider collided woth in form of (pos, shape).
    returns none if no collision'''
    global _physics_world, _aabb_collision

    collider_data = None

    #get nearby colliders
    nearby_colliders = _physics_world.get_nearby_colliders(pos)

    #go through colliders
    for nearby_collider_ent in nearby_colliders:

        #if same entity skip
        if nearby_collider_ent == entity:
            continue

        #get nearby collider data
        nearby_collider_pos = gb.entity_world.component_for_entity(nearby_collider_ent, Position).vector
        nearby_collider_shape = gb.entity_world.component_for_entity(nearby_collider_ent, Shape)

        #if any collide with given collider, get data of collider collided with
        if _aabb_collision(shape, pos, nearby_collider_shape, nearby_collider_pos):
            collider_data = (nearby_collider_pos, nearby_collider_shape)
            break

    return collider_data


def _get_collided_pos(moving_pos = Vector2(), moving_shape = Shape(), collided_pos = Vector2(), collided_shape = Shape()):#TODO fill this out
    '''get the new position of a collider that has collided with another collider'''

    #get move amount for dimensions
    move_amount_x = (moving_shape.width + collided_shape.width) / 2.0 - abs(moving_pos.x - collided_pos.x)
    move_amount_y = (moving_shape.height + collided_shape.height) / 2.0 - abs(moving_pos.y - collided_pos.y)
    #collision moving into vertical surface
    if move_amount_x < move_amount_y:

        #get amount to move on x axis
        delta_pos = math.copysign(move_amount_x, moving_pos.x - collided_pos.x)
        moving_pos.x += delta_pos
        
        #return collision side
        return Vector2(math.copysign(1, delta_pos), 0)

    #collision moving into horizontal surface
    else:
        #get amount to move on y axis
        delta_pos = math.copysign(move_amount_y, moving_pos.y - collided_pos.y)
        moving_pos.y += delta_pos

        #return collision side
        return Vector2(0, math.copysign(1, delta_pos))





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
        global _calculate_normals, _calculate_positions

        _calculate_positions()

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