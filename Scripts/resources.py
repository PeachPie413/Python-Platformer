import global_variables as gb
import pygame as py
import os

#list of all sprite files in the game
sprite_list = []
#dictionary of sprite file name to id
sprite_id_dict = {}

#load all sprites in the game
def load_sprites():
    file_list = os.listdir("Assets")

    #for each file in Assets
    current_id = 0
    for file_name in file_list:
        #add to list
        sprite_list.append(py.image.load('Assets/' + file_name))
        #add to dict
        sprite_id_dict[file_name] = current_id

        current_id += 1


def load_assets():
    load_sprites()