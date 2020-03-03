# Map size
TILE_SIZE = 10
MAP_HEIGHT = 512
MAP_WIDTH = 512

TITLE = "Barf Fortess"
FPS = 30

# Colours
COLOR = { 
    "BLACK" : (0, 0, 0),
    "WHITE" : (255, 255, 255),
    "LIGHTGRAY" : (100, 100, 100),
    "MOUNTAIN" : (70, 70, 70),
    "BOG" : (140, 115, 40),
    "GROUND" : (40, 185, 0),
    "FOREST" : (15, 100, 15),
    "WATER" : (45, 20, 225)
    }

def GridWidth():
    return MAP_WIDTH / TILE_SIZE

def GridHeight():
    return MAP_HEIGHT / TILE_SIZE
