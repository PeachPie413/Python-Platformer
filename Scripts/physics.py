import pygame as py
import global_variables as gb
import esper as e
from core_classes import *



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


    def aabb_collision(self, a_collider = Collider(), a_pos = Position, b_collider = Collider, b_pos = Position()):
        return a_pos.vector.x < b_pos.vector.x + b_collider.width / 2.0 and a_pos.vector.x + a_collider.width / 2.0 > b_pos.vector.x or a_pos.vector.y < b_pos.vector.y + b_collider.height / 2.0 and a_pos.vector.y + a_collider.height / 2.0 > b_pos.vector.y


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
                print('collison!')
            

    '''sets the pos of the collider it is colliding with'''
    def set_collider_pos(self, pos = Vector2(), colliding_colliders = []):
        pass


    def process(self):

        #go through all entities w/ pos, veloc, and collider
        for ent, (pos, veloc, collider) in gb.entity_world.get_components(Position, Velocity, Collider):

            #check if there is a colliding collider
            if colliding_colliders := self.collider_is_colliding(pos, collider, ent):

                #set new pos by colliding, rember to do either vertical or horizontal first
                self.set_collider_pos(pos.vector, colliding_colliders)