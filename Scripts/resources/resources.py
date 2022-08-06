import global_variables as gb
from core_classes import *
import pygame as py
import os
from world_data.world_data import Tile_Type
import json
from resources.globals import *


class Sprite_Metadata:
    def __init__(self, size = Vector2()) -> None:
        self.size = size

#load all sprites in the game
def load_sprites():
    file_list = os.listdir(SPRITE_PATH)

    #for each file in Assets
    current_id = 0
    for file_name in file_list:

        #load image
        sprite = py.image.load(SPRITE_PATH + '/' + file_name)

        #add to lists
        sprite_list.append(sprite)
        sprite_metadata_list.append(Sprite_Metadata(Vector2(sprite.get_width(), sprite.get_height())))
        #add to dict
        sprite_name, seperator, file_type = file_name.partition('.')
        sprite_id_dict[sprite_name] = current_id

        current_id += 1


#load all tile types to a dict
def load_tile_types():
    global tile_type_dict
    global sprite_id_dict

    file_list = os.listdir(TILE_TYPE_PATH)

    #go through all tile types
    for file_name in file_list:
        #open file
        with open(TILE_TYPE_PATH + '/' + file_name, 'r') as f_stream:

            contents = f_stream.read()

            #convert to dict
            json_dict = json.loads(contents)

            #create tile type and fil lit's data
            tile_type = Tile_Type()
            tile_type.sprite = sprite_id_dict[json_dict['sprite']]
            tile_type.collides = json_dict['collides']
            tile_type.id_name = json_dict['id_name']

            #add to dict
            tile_type_dict[json_dict['id_name']] = tile_type
        


def load_assets():
    load_sprites()
    load_tile_types()