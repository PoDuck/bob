from settings import *
from pytmx.util_pygame import load_pygame
import pygame
from pygame.locals import *


class TileMap(object):
    def __init__(self, window):
        self.world_offset = [0, 0]  # Where is player in relation to the starting point
        self.tmx_data = load_pygame("assets/level1.tmx")  # Level map
        self.window = window
        self.solids = []
        self.ground = []
        self.get_collision_objects()
        self.fully_right = False
        self.fully_left = False
        self.fully_up = False
        self.fully_down = False

    def get_collision_objects(self):
        width = self.tmx_data.width
        height = self.tmx_data.height
        tile_width = self.tmx_data.tilewidth
        tile_height = self.tmx_data.tileheight
        self.solids = [[None] * width for i in range(height)]
        for x in range(width):
            for y in range(height):
                obj = self.tmx_data.get_tile_properties(x, y, 0)
                if obj is not None:
                    if obj['solid']:
                        new_rect = pygame.Rect(x * tile_width + self.world_offset[0],
                                               y * tile_height + self.world_offset[1],
                                               tile_width, tile_height)
                        self.solids[y][x] = new_rect

    def get_tile_properties(self, x, y):
        world_x = int(x) - self.world_offset[0]
        world_y = int(y) - self.world_offset[1]
        tile_x = world_x // 32
        tile_y = world_y // 32
        try:
            properties = self.tmx_data.get_tile_properties(tile_x, tile_y, 0)
        except ValueError:
            properties = {"ground": 0, "points": 0, "provides": "", "solid": 0}
        if properties is None:
            properties = {"ground": 0, "points": 0, "provides": "", "solid": 0}
        return properties

    def update(self):
        self.get_collision_objects()

    def move(self, dx, dy):
        self.world_offset[0] -= dx
        # self.world_offset[1] -= dy

    def draw(self):
        for layer in self.tmx_data:
            for tile in layer.tiles():
                x, y, image = tile
                x = x * 32 + self.world_offset[0]
                y = y * 32 + self.world_offset[1]
                self.window.blit(image, (x, y))
