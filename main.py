import pygame
import sys
from map import Map
from player import Player
from opponents import Blinky

WINDOW_SIZE = (570, 630+100)

window = pygame.display.set_mode(WINDOW_SIZE)
screen = pygame.Surface((570, 630))
store_bar = pygame.Surface((570, 100))
pygame.font.init()
level = ['###################',
         '#        #       E#',
         '# ## ### # ### ## #',
         '#                 #',
         '# ## # ##### # ## #',
         '#    #   #   #    #',
         '#### ### # ### ####',
         '#### #       # ####',
         '#### # ##-## # ####',
         '       #***#       ',
         '#### # ##### # ####',
         '#### #       # ####',
         '#### # ##### # ####',
         '#E       #        #',
         '# ## ### # ### ## #',
         '#  #           # E#',
         '## # # ##### # # ##',
         '#    #   #  E#    #',
         '# ###### # ###### #',
         '#E               t#',
         '###################']
punkts = [(240, 240, u'Play', (250, 250, 30), (250, 30, 250), 0),
          (250, 310, u'Quit', (250, 250, 30), (250, 30, 250), 1)]

sprites = pygame.sprite.Group()
x = 0
y = 0
forks = dict()
for row in level:
    for column in row:
        if column is not "*" and column is not "-":
            sprite = Map(x, y, column)
            sprites.add(sprite)
        if column is " " and x != 540 and x != 0:
            direction = [0, 0, 0, 0]
            if level[y//30 - 1][x//30] == " ":
                direction[0] = 1
            if level[y//30][x//30 + 1] == " ":
                direction[1] = 1
            if level[y//30 + 1][x//30] == " ":
                direction[2] = 1
            if level[y//30][x//30 - 1] == " ":
                direction[3] = 1
            forks[str(x) + ',' + str(y)] = direction
        x += 30
    y += 30
    x = 0

eating = pygame.sprite.Group()
pacman = Player(30, 30)
blinky = Blinky(270, 210, pacman, forks)
left = right = up = down = False
sprites.add(pacman)
sprites.add(blinky)


class Menu:
    def __init__(self, punkts=([120, 140, u'Punkts', (250, 250, 30), (250, 30, 250), 0],)):
        self.punkts = punkts

    def render(self, surface, font, num_punkt):
        for i in self.punkts:
            if num_punkt == i[5]:
                surface.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                surface.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))

    def menu(self):
        done = True
        font_menu = pygame.font.Font('fonts/orbitron-light.ttf', 50)
        punkt = 0
        while done:
            screen.fill((0, 100, 200))
            mp = pygame.mouse.get_pos()
            for i in self.punkts:
                if mp[0] > i[0] and mp[0] < i[0]+155 and mp[1] > i[1] and mp[1] < i[1]+50:
                      punkt = i[5]
            self.render(screen, font_menu, punkt)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        sys.exit()
                    if e.key == pygame.K_UP:
                        if punkt > 0:
                            punkt -= 1
                    if e.key == pygame.K_DOWN:
                        if punkt < len(self.punkts) - 1:
                            punkt += 1
                    if e.key == pygame.K_RETURN:
                        if punkt == 0:
                            done = False
                        elif punkt == 1:
                            sys.exit()
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if punkt == 0:
                        done = False
                    elif punkt == 1:
                        sys.exit()
            window.blit(screen, (0, 0))
            pygame.display.flip()


def play():
    left = right = up = down = False
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    left = True
                    right = up = down = False
                if e.key == pygame.K_RIGHT:
                    right = True
                    left = up = down = False
                if e.key == pygame.K_UP:
                    up = True
                    left = right = down = False
                if e.key == pygame.K_DOWN:
                    down = True
                    left = right = up = False
                if e.key == pygame.K_ESCAPE:
                    paused()
        if pacman.is_win:
            win()
        if pacman.is_lose:
            lose()
        pacman.update(left, right, up, down)
        blinky.update()
        screen.fill((0, 0, 0))
        eating.draw(screen)
        sprites.draw(screen)
        window.blit(screen, (0, 0))
        window.blit(store_bar, (0, 630))
        if pacman.lifes == 3:
            life = pygame.image.load('images/status_bar/life3.png')
        elif pacman.lifes == 2:
            life = pygame.image.load('images/status_bar/life2.png')
        elif pacman.lifes == 1:
            life = pygame.image.load('images/status_bar/life1.png')
        else:
            life = pygame.image.load('images/status_bar/life.png')
        store_bar.blit(life, (20, 50))
        screen.fill((0, 0, 0))
        pygame.display.flip()
        pygame.time.delay(1)


def paused():
    pause = True
    pygame.time.wait(1000)
    font = pygame.font.Font('fonts/orbitron-light.ttf', 50)
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.time.wait(1000)
                    pause = False
        window.blit(screen, (0, 0))
        screen.fill((0, 0, 0))
        screen.blit(font.render("Pause", 1, (255, 255, 255)), (235, 280))
        pygame.display.flip()
        pygame.time.delay(1)


def win():
    font = pygame.font.Font('fonts/orbitron-light.ttf', 30)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        window.blit(screen, (0, 0))
        screen.fill((0, 0, 0))
        screen.blit(font.render("YOU WIN!!!", 1, (255, 255, 255)), (150, 280))
        screen.blit(font.render("YOUR SCORE: " + str(pacman.score), 1, (255, 255, 255)), (10, 340))
        pygame.display.flip()
        pygame.time.delay(1)


def lose():
    font = pygame.font.Font('fonts/orbitron-light.ttf', 30)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        window.blit(screen, (0, 0))
        screen.fill((0, 0, 0))
        screen.blit(font.render("YOU LOSE )=", 1, (255, 255, 255)), (120, 280))
        screen.blit(font.render("YOUR SCORE: " + str(pacman.score), 1, (255, 255, 255)),
        (10, 340))
        pygame.display.flip()
        pygame.time.delay(1)


game = Menu(punkts)
while True:
    game.menu()
    play()
