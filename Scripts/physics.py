from pygame import Vector2
import global_variables as gb
import esper as e
from core_classes import *



class Velocity(Vector2):
    pass
    
class Acceleration(Vector2):
    pass

class Collider:
    def __init__(self) -> None:
        pass



class Acceleration_Processor(e.Processor):

    def process(self):
        for entity, (vel, acc) in gb.entity_world.get_components(Velocity, Acceleration):
            vel += acc


class Velocity_Processor(e.Processor):

    def process(self):

        #go through all entities w/ pos, veloc, and collider

            #check if there is a colliding collider

            #if colliding

                #set new pos by colliding, rember to do either vert or hrt first



        pass