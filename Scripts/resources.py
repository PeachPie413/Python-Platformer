import global_variables as gb
import pygame as py
import os

#list of all sprite files in the game
sprite_list = []

#load all sprites in the game
def load_sprites():
    file_list = os.listdir("Assets")

    #for each file in Assets
    for file_name in file_list:
        sprite_list.append(py.image.load('Assets/' + file_name))


def load_assets():
    load_sprites()