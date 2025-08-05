from pygame import *
from random import randint

score = 0
lost = 0
win_width, win_height = 1400,800
"""СЦЕНА"""
window = display.set_mode((win_width, win_height))
display.set_caption('Шутер')
background = transform.scale(image.load('C:/prod/Пт17/shooter/galaxy.jpg'), (win_width, win_height))
clock = time.Clock()

"""Музика"""
mixer.init()
mixer.music.load('tunetank.com_1585_space_by_finval.mp3')
mixer.music.set_volume(0.05)
mixer.music.play()
fire = mixer.Sound('fire.ogg')

"""Шрифти"""
font.init()
font1 = font.SysFont('Robot', 50)
font2 = font.SysFont('Robot', 110)

"""КЛАСИ"""
class GameSprite(sprite.Sprite):
    def __init__(self, img= None, x= 0, y= 0, width= 0, height= 0, speed= 0):
        sprite.Sprite.__init__(self)
        if img:
            self.image = transform.scale(image.load(img), (width, height))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        else:
            self.rect = Rect(x,y, width, height)
        self.top = True
        self.bottom = True
        self.left = True
        self.right = True
        self.speed = speed
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def fill(self):
        draw.rect(window, (255,0,0), self.rect)

class Player(GameSprite):
    def update(self):
        self.reset()
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - self.rect.width:
            self.rect.x += self.speed

class Enemy(GameSprite):
    def update(self):
        global lost
        self.reset()
        self.rect.y += self.speed
        if self.rect.y > win_height:
            lost += 1
            self.rect.y = -100
            self.rect.x = randint(0, win_width - 80)
            self.speed = randint(1,5)

class Asteroid(GameSprite):
    def update(self):
        self.reset()
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = -100
            self.rect.x = randint(0, win_width - 80)
            self.speed = randint(1, 5)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Asteroid('C:/prod/Пт17/shooter/asteroid.png', randint(0, win_width - 80), -100, 80, 50, randint(1,5))
    asteroids.add(asteroid)


player = Player('C:/prod/Пт17/shooter/rocket.png', win_width / 2 - 80, win_height - 120, 80, 100, 5)
enemies = sprite.Group()
for i in range(5):
    enemy = Enemy('C:/prod/Пт17/shooter/ufo.png', randint(0, win_width - 80), -100, 80, 50, randint(1,5))
    enemies.add(enemy)


run = True
finish = False
while run:
    for e in event.get():
        if e.type == QUIT:
            quit()
    window.blit(background, (0,0))
    player.update()
    enemies.update()
    asteroids.update()

    score_label = font1.render('Рахунок: ' + str(score), True, (255, 255, 255))
    lost_label = font1.render('Пропущено: ' + str(lost), True, (255,255,255))
    window.blit(lost_label, (10, 100))
    window.blit(score_label, (10, 50))

    display.update()
    clock.tick(60)