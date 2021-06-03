from outlined_text import OutlinedText


class Stats(object):
    """
    show game stats at top of screen evenly spaced
    """
    def __init__(self, player, screen):
        self.player = player
        self.screen = screen
        self.titles = [
            OutlinedText(text='SCORE', position=(100, 2), outline_width=2, font_size=20, screen=self.screen),
            OutlinedText(text='COINS', position=(200, 2), outline_width=2, font_size=20, screen=self.screen),
            OutlinedText(text='WORLD', position=(300, 2), outline_width=2, font_size=20, screen=self.screen),
            OutlinedText(text='TIME', position=(400, 2), outline_width=2, font_size=20, screen=self.screen),
            OutlinedText(text='LIVES', position=(400, 2), outline_width=2, font_size=20, screen=self.screen),
        ]
        self.stats = []
        for i in range(len(self.titles)):
            self.stats.append(
                OutlinedText(text='0', position=(100 + i * 100, 2), outline_width=2, font_size=20, screen=self.screen)
            )
        self.centers = self.center_spacing(self.titles, 2)
        self.center_spacing(self.stats, 25, self.centers)

    # center the spacing between the text.  If you give a spacing array (centers of text), it will center to the points
    # in that array of points of tuple (x, y).  y_offset is distance from top of screen.
    def center_spacing(self, text_array, y_offset, spacing_array=None):
        center_spacing = []
        if not spacing_array:
            total_width = 0
            for text in text_array:
                total_width += text.get_width()
            text_spacing = (self.screen.get_width() - total_width) // (len(self.titles) + 1)
            start_x = text_spacing
            for text in text_array:
                center_spacing.append(start_x + text.get_width() // 2)
                text.change_position((start_x, y_offset))
                start_x += text.get_width() + text_spacing
            return center_spacing
        else:
            for i in range(len(text_array)):
                start_x = spacing_array[i] - text_array[i].get_width() // 2
                text_array[i].change_position((start_x, y_offset))

    # update stats
    def update_score(self, score):
        self.center_spacing(self.stats, 25, self.centers)
        self.stats[0].change_text(score)

    def update_coins(self, coins):
        self.center_spacing(self.stats, 25, self.centers)
        self.stats[1].change_text(coins)

    def update_world(self, world):
        self.center_spacing(self.stats, 25, self.centers)
        self.stats[2].change_text(world)

    def update_time(self, time):
        self.center_spacing(self.stats, 25, self.centers)
        self.stats[3].change_text(time)

    def update_lives(self, lives):
        self.center_spacing(self.stats, 25, self.centers)
        self.stats[4].change_text(lives)

    def draw(self):
        for title in self.titles:
            title.draw()
        for stat in self.stats:
            stat.draw()
