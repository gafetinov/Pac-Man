from pygame.sprite import Sprite, collide_rect, collide_mask
from pygame.image import load
import map
import math

SPEED = 1


class Blinky(Sprite):
    def __init__(self, x, y, target, forks):
        Sprite.__init__(self)
        self.image = load('images/ghosts/blinky.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dx = 0
        self.dy = 0
        self.target = target
        self.forks = forks
        self.is_hunting = False

    def update(self):
        if self.is_hunting:
            self.hunt()
        else:
            self.wander()
        if self.target.is_invincible:
            self.is_hunting = False
            self.is_scared = True
            self.image = load('images/ghosts/scared.png')
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.collide(map.WALLS)
        self.teleport()
        self.killing()

    def collide(self, walls):
        for wall in walls:
            if collide_rect(self, wall):
                if self.dx > 0:
                    self.rect.right = wall.rect.left
                elif self.dx < 0:
                    self.rect.left = wall.rect.right+1
                elif self.dy > 0:
                    self.rect.bottom = wall.rect.top
                elif self.dy < 0:
                    self.rect.top = wall.rect.bottom

    def killing(self):
        if collide_mask(self.target, self):
            if self.is_hunting:
                if self.target.lifes < 1:
                    self.target.kill()
                    self.target.is_lose = True
                self.target.rect.x = 30
                self.target.rect.y = 30
                self.target.lifes -= 1
            elif self.is_scared:
                self.image = load('images/ghosts/blinky.png')
                self.rect.x = 270
                self.rect.y = 210
                self.is_hunting = True
                self.target.is_invincible = False

    def wander(self):
        if (self.rect.x == 300 and self.rect.y == 210) or (self.rect.x == 360 and self.rect.y == 150) or (self.rect.x == 510 and self.rect.y == 90):
            self.dy = -SPEED
            self.dx = 0
        elif (self.rect.x == 300 and self.rect.y == 150) or (self.rect.x == 360 and self.rect.y == 90) or (self.rect.x == 270 and self.rect.y == 210):
            self.dx = SPEED
            self.dy = 0
        elif self.rect.x == 510 and self.rect.y == 30:
            self.dx = -SPEED
            self.dy = 0
            self.is_hunting = True


    def hunt(self):
        if (str(self.rect.x) + "," + str(self.rect.y)) in self.forks:
            fork = self.forks[str(self.rect.x) + "," + str(self.rect.y)]
            distanceX = self.rect.x - self.target.rect.x
            distanceY = self.rect.y - self.target.rect.y
            if math.fabs(distanceX) < math.fabs(distanceY):
                if distanceY > 0:
                    if fork[0] == 1 and self.dy != -SPEED:
                        self.dy = -SPEED
                        self.dx = 0
                    else:
                        self.goFree(fork)
                else:
                    if fork[2] == 1 and self.dy != SPEED:
                        self.dy = SPEED
                        self.dx = 0
                    else: self.goFree(fork)
            else:
                if distanceX > 0:
                    if fork[3] == 1 and self.dx != SPEED:
                        self.dx = -SPEED
                        self.dy = 0
                    else: self.goFree(fork)
                else:
                    if fork[1] == 1 and self.dx != -SPEED:
                        self.dx = SPEED
                        self.dy = 0
                    else: self.goFree(fork)


    def goFree(self, fork):
        if fork[0] == 1 and self.dy != SPEED:
            self.dy = -SPEED
            self.dx = 0
        elif fork[1] == 1 and self.dx != -SPEED:
            self.dx = SPEED
            self.dy = 0
        elif fork[2] == 1 and self.dy != SPEED:
            self.dy = SPEED
            self.dx = 0
        elif fork[3] == 1 and self.dx != -SPEED:
            self.dx = -SPEED
            self.dy = 0


    def teleport(self):
        if self.rect.x < -20 and self.rect.y == 270 and self.dx < 0:
            self.rect.x = 620
            self.rect.y = 270
        elif self.rect.x > 620 and self.rect.y == 270 and self.dx > 0:
            self.rect.x = -20
            self.rect.y = 270