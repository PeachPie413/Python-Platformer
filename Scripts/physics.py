import pygame as py
import global_variables as gb
import esper as e
from core_classes import *
import math



class Velocity(Vector2):
    pass
    
class Acceleration(Vector2):
    pass

class Collider:
    def __init__(self, width = 0, height = 0):
        self.width = width
        self.height = height
        



class Acceleration_Processor(e.Processor):

    def process(self):
        for entity, (vel, acc) in gb.entity_world.get_components(Velocity, Acceleration):
            vel += acc



class Velocity_Processor(e.Processor):


    def aabb_collision(self, a_collider = Collider(), a_pos = Position(), b_collider = Collider(), b_pos = Position()):
        a_max_x = a_pos.vector.x + a_collider.width / 2.0
        a_min_x = a_pos.vector.x - a_collider.width / 2.0
        b_max_x = b_pos.vector.x + b_collider.width / 2.0
        b_min_x = b_pos.vector.x - b_collider.width / 2.0
        a_max_y = a_pos.vector.y + a_collider.height / 2.0
        a_min_y = a_pos.vector.y - a_collider.height / 2.0
        b_max_y = b_pos.vector.y + b_collider.height / 2.0
        b_min_y = b_pos.vector.y - b_collider.height / 2.0
        return a_max_x > b_min_x and b_max_x > a_min_x and a_max_y > b_min_y and b_max_y > a_min_y

    '''returns the collider(s) it is colliding with'''
    def collider_is_colliding(self, self_pos = Position(), self_collider = Collider(), self_ent = 0):

        #create list of things collided with
        collidied_colliders = []

        #go through all possible things to collide wit
        for ent, (pos, collider) in gb.entity_world.get_components(Position, Collider):

            #skip if the collider is the colliding one
            if(ent == self_ent): continue

            #check if they are colliding
            if(self.aabb_collision(collider, pos, self_collider, self_pos)):
                collidied_colliders.append((collider, pos))

        return collidied_colliders
            

    def try_set_pos_collision(self, pos = Vector2(), collider = Collider(), colliding_collider = Collider(), colliding_pos = Vector2(), min_pos_change = 0.0):

        #get move amount for dimensions
        move_amount_x = (collider.width + colliding_collider.width) / 2.0 - abs(pos.x - colliding_pos.x)
        move_amount_y = (collider.height + colliding_collider.height) / 2.0 - abs(pos.y - colliding_pos.y)

        #collision on width
        if move_amount_x < move_amount_y:
            #get amount to move on x axis
            pos.x += math.copysign(move_amount_x, pos.x - colliding_pos.x)
        #collision on height
        else:
            #get amount to move on x axis
            pos.y += math.copysign(move_amount_y, pos.y - colliding_pos.y)

    '''sets the pos of the collider it is colliding with'''
    def set_collider_pos(self, pos = Vector2(), self_collider = Collider(), colliding_colliders = []):
        
        min_pos_change = 100.0

        #go through all collided colliders
        for (collider, collider_pos) in colliding_colliders:
            self.try_set_pos_collision(pos, self_collider, collider, collider_pos.vector, min_pos_change)


    def process(self):

        #go through all entities w/ pos, veloc, and collider
        for ent, (pos, veloc, collider) in gb.entity_world.get_components(Position, Velocity, Collider):

            #check if there is a colliding collider
            if colliding_colliders := self.collider_is_colliding(pos, collider, ent):

                #set new pos by colliding, rember to do either vertical or horizontal first
                self.set_collider_pos(pos.vector, collider, colliding_colliders)