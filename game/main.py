import pygame
from pygame.locals import *
from tiles import TileMap
from settings import *
from player import Player
from menu import StartMenu, RestartMenu
from stats import Stats


class Game(object):
    def __init__(self):
        # Initialize
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()
        pygame.time.set_timer(USEREVENT, 1000)
        self.level_counter = LEVEL_TIME
        # initialize the map
        self.tiles = TileMap(self.screen)
        # initialize start menu
        self.menu = StartMenu(self.screen)
        # initialize restart menu
        self.restart_menu = RestartMenu(self.screen)
        # initialize player
        self.bob = Player(char_type='bob', x=140, y=self.screen.get_height() - 85,
                          scale=PLAYER_SCALE, speed=NORMAL_SPEED, screen=self.screen, tiles=self.tiles)
        self.run = True
        self.start_game = False
        # initialize stats
        self.stats = Stats(self.bob, self.screen)

        while self.run:
            if not self.start_game:
                # main menu
                self.screen.fill(BG)
                menu_res = self.menu.draw()
                if menu_res == 1:
                    self.start_game = True
                elif menu_res == 2:
                    self.run = False
            else:
                self.update()
                self.move()
                self.draw()
            self.events()
            pygame.display.flip()
        pygame.quit()

    def update(self):
        self.clock.tick(FPS)
        self.draw_bg(BG)
        if not self.bob.update():
            self.tiles.update()
        self.stats.update_lives(str(self.bob.lives))
        self.stats.update_score(str(self.bob.score))
        self.stats.update_coins(str(self.bob.coins))
        self.stats.update_time(str(self.bob.time))
        self.stats.update_world(str(self.bob.world))

    def events(self):
        for event in pygame.event.get():
            # quit game
            if event.type == QUIT:
                self.run = False

            if event.type == USEREVENT:
                self.bob.time -= 1

            # keyboard events
            if event.type == pygame.KEYDOWN:
                if event.key == K_LEFT:
                    self.bob.moving_left = True
                if event.key == K_RIGHT:
                    self.bob.moving_right = True
                if event.key == K_SPACE and self.bob.alive:
                    if not self.bob.in_air:
                        self.bob.jump = True
                if event.key == K_ESCAPE:
                    self.run = False
                if event.key == K_LCTRL:
                    self.bob.speed_pressed = True

            # keyboard button released
            if event.type == pygame.KEYUP:
                if event.key == K_LEFT:
                    self.bob.moving_left = False
                if event.key == K_RIGHT:
                    self.bob.moving_right = False
                if event.key == K_LCTRL:
                    self.bob.speed_pressed = False

    def move(self):
        self.bob.move()
        self.tiles.move(self.bob.scroll_x, self.bob.scroll_y)

    def draw(self):
        self.tiles.draw()
        self.bob.draw()
        self.stats.draw()

    def draw_bg(self, bg):
        self.screen.fill(pygame.Color(bg))
        self.tiles.update()
        self.bob.update()


def main():
    game = Game()


if __name__ == "__main__":
    main()
