from settings import *
import glob
import pygame
from pygame.locals import *


class Character(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, screen, tiles):
        pygame.sprite.Sprite.__init__(self)
        self.initial_x = x
        self.initial_y = y
        self.alive = True
        self.char_type = char_type
        self.scale = scale
        self.speed = speed
        self.distance = 0
        self.direction = 1
        self.moving_left = False
        self.moving_right = False
        self.vel_y = 0
        self.in_air = True
        self.flip = False
        self.screen = screen
        self.tiles = tiles
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.dead = False
        self.dx = 0
        self.dy = 0

        # load all images for players
        animation_types = ['idle', 'run', 'jump', 'climb']
        for animation in animation_types:
            # reset temporary images
            temp_list = []
            # count num of frames in folder
            num_frames = len(glob.glob(f'assets/images/{self.char_type}/{animation}*.png'))
            for i in range(num_frames):
                img = pygame.image.load(f'assets/images/{self.char_type}/{animation}{i}.png')
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset_character(self):
        self.rect.x = self.initial_x
        self.rect.y = self.initial_y
        self.alive = True
        self.frame_index = 0
        self.moving_left = False
        self.moving_right = False
        self.image = self.animation_list[0][self.frame_index]

    def update_action(self, new_action):
        # check if new action is different to previous action
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def move(self):
        self.dx = 0
        self.dy = 0

        if self.moving_left:
            self.dx -= self.speed
            self.distance += self.speed
            self.flip = True
            self.direction = -1

        if self.moving_right:
            self.dx += self.speed
            self.distance -= self.speed
            self.flip = False
            self.direction = 1

        # apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        self.dy += self.vel_y

        # check for collision
        for x in range(len(self.tiles.solids)):
            for y in range(len(self.tiles.solids[x])):
                if self.tiles.solids[x][y] is not None:
                    tile = self.tiles.solids[x][y]  # rectangle blocking object
                    # x collisions
                    if tile.colliderect(self.rect.x + self.dx, self.rect.y, self.rect.width, self.rect.height):
                        if self.dx < 0:
                            self.dx = self.rect.left - tile.right
                            if self.dx > 0:
                                self.dx = 0
                        elif self.dx > 0:
                            self.dx = tile.left - self.rect.right
                            if self.dx < 0:
                                self.dx = 0
                        else:
                            self.dx = 0
                    # y collisions
                    if tile.colliderect(self.rect.x, self.rect.y + self.dy, self.rect.width, self.rect.height):
                        # if jumping
                        if self.vel_y < 0:
                            self.vel_y = 0
                            self.dy = tile.bottom - self.rect.top
                        # if falling
                        elif self.vel_y >= 0:
                            self.vel_y = 0
                            self.in_air = False
                            self.dy = tile.top - self.rect.bottom
                    # Don't allow jumping if character walks off a block
                    elif self.vel_y > GRAVITY:
                        self.in_air = True

        # check if going off edges
        if self.rect.left + self.dx < 0 or self.rect.right + self.dx > self.screen.get_width():
            self.dx = 0

        # kill if if character falls off screen
        if self.rect.top + self.dy > self.screen.get_height():
            self.alive = False

        # update character position
        self.rect.x += self.dx
        self.rect.y += self.dy

    def update(self):
        if self.alive:
            # select image
            self.image = self.animation_list[self.action][self.frame_index]

            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
            if self.frame_index >= len(self.animation_list[self.action]):
                if self.action == 3:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                else:
                    self.frame_index = 0

                    # update animation action
                    if self.alive:
                        if self.in_air:
                            self.update_action(2)
                        elif self.moving_left or self.moving_right:
                            self.update_action(1)
                        else:
                            if self.action != 2:
                                self.animation_list[0][0] = self.animation_list[self.action][
                                    self.frame_index]
                            self.update_action(0)

    def draw(self):
        if self.alive:
            self.screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
