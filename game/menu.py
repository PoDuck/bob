from button import Button
import pygame


class Menu(object):
    def __init__(self, screen):
        self.screen = screen

    def draw(self):
        pass


class StartMenu(Menu):
    def __init__(self, screen):
        self.screen = screen
        # load button images
        self.start_img = pygame.image.load('assets/images/bob/menu/start_btn.png').convert_alpha()
        self.exit_img = pygame.image.load('assets/images/bob/menu/exit_btn.png').convert_alpha()
        self.start_button = Button(self.screen.get_width() // 2 - 130, self.screen.get_height() // 2 - 150,
                                   self.start_img, 1)
        self.exit_button = Button(self.screen.get_width() // 2 - 110, self.screen.get_height() // 2 - 30, self.exit_img,
                                  1)
        super(StartMenu, self).__init__(screen)

    def draw(self):
        if self.start_button.draw(self.screen):
            return 1
        if self.exit_button.draw(self.screen):
            return 2


class RestartMenu(Menu):
    def __init__(self, screen):
        self.screen = screen
        self.restart_img = pygame.image.load('assets/images/bob/menu/restart_btn.png').convert_alpha()
        self.restart_button = Button(self.screen.get_width() // 2 - 130, self.screen.get_height() // 2 - 150,
                                   self.restart_img, 2)
        super(RestartMenu, self).__init__(screen)

    def draw(self):
        return self.restart_button.draw(self.screen)
