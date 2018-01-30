from pygame.sprite import Sprite, collide_rect, collide_mask
from pygame.image import load
import map

SPEED = 1
PLAYER_TO_RIGHT = load('images/pacman/right.png')
PLAYER_TO_LEFT = load('images/pacman/left.png')
PLAYER_TO_UP = load('images/pacman/up.png')
PLAYER_TO_DOWN = load('images/pacman/down.png')


class Player(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = PLAYER_TO_RIGHT
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dx = 0
        self.dy = 0
        self.score = 0
        self.is_invincible = False
        self.lifes = 3
        self.is_win = False
        self.is_lose = False
        self.timer = 0

    def update(self, left, right, up, down):
        if self.rect.y % 30 == 0:
            if left:
                self.dx = -SPEED
                self.dy = 0
                self.image = PLAYER_TO_LEFT
            elif right:
                self.dx = SPEED
                self.dy = 0
                self.image = PLAYER_TO_RIGHT
        if self.rect.x % 30 == 0:
            if up:
                self.dy = -SPEED
                self.dx = 0
                self.image = PLAYER_TO_UP
            elif down:
                self.dy = SPEED
                self.dx = 0
                self.image = PLAYER_TO_DOWN
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.collide()
        self.eating()
        self.get_energy()
        self.teleport()

    def collide(self):
        for wall in map.WALLS:
            if collide_rect(self, wall):
                if self.dx > 0:
                    self.rect.right = wall.rect.left
                elif self.dx < 0:
                    self.rect.left = wall.rect.right+1
                elif self.dy > 0:
                    self.rect.bottom = wall.rect.top
                elif self.dy < 0:
                    self.rect.top = wall.rect.bottom

    def eating(self):
        for x in range(len(map.FOODS)):
            if collide_mask(self, map.FOODS[x]):
                map.FOODS.pop(x).kill()
                self.score += 100
                if len(map.FOODS) == 0:
                    self.is_win = True
                break

    def teleport(self):
        if self.rect.x < -20 and self.rect.y == 270 and self.dx < 0:
            self.rect.x = 620
            self.rect.y = 270
        elif self.rect.x > 620 and self.rect.y == 270 and self.dx > 0:
            self.rect.x = -20
            self.rect.y = 270

    def get_energy(self):
        energizers = map.ENERGIZERS
        for x in range(len(energizers)):
            if collide_mask(self, energizers[x]):
                energizers.pop(x).kill()
                self.score += 100
                self.is_invincible = True
                break