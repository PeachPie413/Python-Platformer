from core_classes import *
import global_variables as gb



CHUNK_SIZE = 32
CHUNK_CHANGED_EVENT_NAME = 'chunk_changed'
CHUNK_CREATED_EVENT_NAME = 'chunk_loaded'
CHUNK_DESTROYED_EVENT_NAME = 'chunk_destroyed'



class Chunk:
    def __init__(self, chunk_pos = Vector2()) -> None:
        self.tile_data = Grid()
        self.pos = chunk_pos

class Zone: