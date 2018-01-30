from pygame.sprite import Group, Sprite
from pygame.image import load

WALLS = []
FOODS = []
ENERGIZERS = []
TIME_TRAPS = []

class Map(Sprite):
    def __init__(self, x, y, element):
        Sprite.__init__(self)
        self.image = load('images/map/wall.png')
        if element == '#':
            WALLS.append(self)
        elif element == ' ':
            self.image = load('images/map/food.png')
            FOODS.append(self)
        elif element == 'E':
            self.image = load('images/map/energizer.png')
            ENERGIZERS.append(self)
        elif element == 't':
            TIME_TRAPS.append(self)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y