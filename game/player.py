from settings import *
import pygame
from pygame.locals import *
from character import Character
from menu import RestartMenu


class Player(Character):
    def __init__(self, char_type, x, y, scale, speed, screen, tiles):
        super().__init__(char_type, x, y, scale, speed, screen, tiles)
        self.lives = 3
        self.score = 0
        self.world = '1-1'
        self.coins = 0
        self.time = LEVEL_TIME
        self.jump = False
        self.scroll_x = 0
        self.scroll_y = 0
        self.restart_menu = RestartMenu(self.screen)
        # if game needs to be reset to play, self.reset = True
        self.reset = False
        self.old_speed = self.speed
        self.speed_pressed = False

    def right_side_hit(self):
        # has player reached the scroll threshold on right side of screen
        return self.rect.right > self.screen.get_width() - SCROLL_THRESHOLD

    def left_side_hit(self):
        # has player reached the scroll threshold on left side of screen
        return self.rect.left < SCROLL_THRESHOLD

    def right_scroll_hit(self):
        # has background scroll reached far right
        return abs(self.tiles.world_offset[0]) < \
               self.tiles.tmx_data.width * self.tiles.tmx_data.tilewidth - self.screen.get_width()

    def left_scroll_hit(self):
        # has the background scroll reached the far left
        return abs(self.tiles.world_offset[0]) > abs(self.dx)

    def reset_character(self):
        # Reset the world and character position to starting point.
        self.tiles.world_offset[0] = self.tiles.world_offset[1] = 0
        self.time = LEVEL_TIME
        super(Player, self).reset_character()

    def change_speed(self):
        # slowly ramp up or down speed in response to speedup button until fast or normal speed hit
        if self.speed_pressed and self.speed < FAST_SPEED and not self.in_air:
            self.speed += 1
        if not self.speed_pressed and self.speed > NORMAL_SPEED and not self.in_air:
            self.speed -= 1

    def update(self):
        if self.time <= 0:
            self.alive = False
            self.time = 0
        self.change_speed()
        # if player died:
        if not self.alive:
            self.lives -= 1
            self.reset_character()
            # if game over
            if self.lives == 0:
                self.reset = True
                self.reset_character()
                # return False if game is over
                return False
        super(Player, self).update()
        # return True if game is still going
        return True

    def move(self):
        # if game not waiting to restart
        if not self.reset:
            self.scroll_x = 0
            self.scroll_y = 0
            # process jump
            if self.jump and not self.in_air:
                self.vel_y = JUMP_HEIGHT
                self.jump = False
                self.in_air = True
            # move character before tiles
            super().move()

            # only scroll if edges of scroll are hit
            if (self.right_side_hit() and self.right_scroll_hit()) or (self.left_side_hit() and self.left_scroll_hit()):
                self.rect.x -= self.dx
                self.scroll_x = self.dx

    def draw(self):
        # if game is over draw restart menu button.
        if self.reset:
            if self.restart_menu.draw():
                self.reset = False
                self.lives = 3
        else:  # if game is not over, draw player
            super(Player, self).draw()

