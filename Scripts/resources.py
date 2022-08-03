import global_variables as gb
from core_classes import *
import pygame as py
import os


class Sprite_Metadata:
    def __init__(self, size = Vector2()) -> None:
        self.size = size



#list of all sprite files in the game
sprite_list = []
#dictionary of sprite file name to id
sprite_id_dict = {}
#list of sprite data, ex width, height in a list so it can be quickyl read w/out loading the whole image
sprite_metadata_list = []
#dict of tile types, use tile type name to get data
tile_type_dict = {}

#load all sprites in the game
def load_sprites():
    file_list = os.listdir("Assets/Sprites")

    #for each file in Assets
    current_id = 0
    for file_name in file_list:

        #load image
        sprite = py.image.load('Assets/' + file_name)

        #add to lists
        sprite_list.append(sprite)
        sprite_metadata_list.append(Sprite_Metadata(Vector2(sprite.get_width(), sprite.get_height())))
        #add to dict
        sprite_id_dict[file_name] = current_id

        current_id += 1


#load all tile types to a dict
def load_tile_types():
    pass
    #use json to save tile types


def load_assets():
    load_sprites()