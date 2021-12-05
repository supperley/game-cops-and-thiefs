# -----------------------------------------------------------------------------
#
# Dodge The Cop!
# Language - Python
# Modules - pygame, sys, random, math
#
# Controls - Mouse Movement
#
#
# -----------------------------------------------------------------------------

import pygame
import sys
import random
from math import *

pygame.init()

width = 500
height = 600
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dodge The Cop!")
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()

background = (51, 51, 51)
playerColor = (249, 231, 159)

red = (203, 67, 53)
yellow = (241, 196, 15)
blue = (46, 134, 193)
green = (34, 153, 84)
purple = (136, 78, 160)
orange = (214, 137, 16)

colors = [red, yellow, blue, green, purple, orange]

score = 0

fon = pygame.image.load('bg.jpg')


class Cop(pygame.sprite.Sprite):
    def __init__(self, speed):
        super(Cop, self).__init__()
        self.x = 0
        self.y = 0
        self.w = 20
        self.h = self.w
        self.speed = speed
        self.angle = 0
        self.screen = display
        self.image = pygame.image.load('cop.png')
        self.rect = self.image.get_rect()  # преобразовали в прямоугольник

    def create_cop(self):
        self.x = width / 2
        self.y = height / 2
        # self.color = random.choice(colors)
        self.angle = random.randint(-180, 180)

    def move(self):
        self.rect.x += self.speed * cos(radians(self.angle))
        self.rect.y += self.speed * sin(radians(self.angle))

        if self.rect.x < 0 or self.rect.x > width - self.rect.width:
            self.angle = 180 - self.angle
        if self.rect.y < 0 or self.rect.y > height - self.rect.height:
            self.angle *= -1

    def draw(self):  # вывод пришельца на экран
        display.blit(self.image, self.rect)  # обращаемся к экрану и вызываем метод блит,
        # который отрисовывает и выводит, мы ему передаем наше изображение и выводим как прямоугольник

    def collision(self, radius):
        pos = pygame.mouse.get_pos()

        dist = ((pos[0] - self.rect.x) ** 2 + (pos[1] - self.rect.y) ** 2) ** 0.5

        if dist <= radius:
            gameOver()


class Thief:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.w = 20
        self.h = self.w
        self.screen = display  # получаем экран
        self.image = pygame.image.load('thief.png')  # загрузили изображение
        self.rect = self.image.get_rect()  # получили картинку как объект rect, то есть прямоугольник

    def generateNewCoord(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        self.screen.blit(self.image, self.rect)  # метод блит отрисовывает нашу пушку


class Money:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.w = 20
        self.h = self.w
        self.screen = display  # получаем экран
        self.image = pygame.image.load('money.png')  # загрузили изображение
        self.rect = self.image.get_rect()  # получили картинку как объект rect, то есть прямоугольник

    def generateNewCoord(self):
        self.rect.x = random.randint(self.rect.width, width - self.rect.width)
        self.rect.y = random.randint(self.rect.height, height - self.rect.height)

    def draw(self):
        self.screen.blit(self.image, self.rect)  # метод блит отрисовывает нашу пушку


def gameOver():
    loop = True

    font = pygame.font.SysFont("Agency FB", 100)
    text = font.render("Game Over!", True, (230, 230, 230))

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_r:
                    gameLoop()
                if event.key == pygame.K_SPACE:
                    gameLoop()

        display.fill(background)

        display.blit(text, (20, height / 2 - 100))
        displayScore()

        pygame.display.update()
        clock.tick()


def checkCollision(target, d, objMoney):
    pos = pygame.mouse.get_pos()
    dist = ((pos[0] - target[0] - objMoney.w) ** 2 + (pos[1] - target[1] - objMoney.h) ** 2) ** 0.5

    if dist <= d + objMoney.w:
        return True
    return False


def close():
    pygame.quit()
    sys.exit()


def displayScore():
    font = pygame.font.SysFont("Forte", 30)
    scoreText = font.render("Score: " + str(score), True, (230, 230, 230))
    display.blit(scoreText, (10, 10))


def gameLoop():
    global score
    score = 0

    loop = True

    pRadius = 15

    thief = Thief()

    balls = []

    for i in range(1):
        newCop = Cop(5)
        newCop.create_cop()
        balls.append(newCop)

    target = Money()
    target.generateNewCoord()
    thief.generateNewCoord(200, 200)

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_r:
                    gameLoop()

        display.blit(fon, (0, 0))

        for i in range(len(balls)):
            balls[i].move()

        for i in range(len(balls)):
            balls[i].draw()

        for i in range(len(balls)):
            balls[i].collision(pRadius)

        playerPos = pygame.mouse.get_pos()
        thief.generateNewCoord(playerPos[0], playerPos[1])

        collide = checkCollision((target.rect.x, target.rect.y), pRadius, target)

        if collide:
            score += 1
            target.generateNewCoord()
        elif score == 2 and len(balls) == 1:
            newCop = Cop(5)
            newCop.create_cop()
            balls.append(newCop)
            target.generateNewCoord()
        elif score == 5 and len(balls) == 2:
            newCop = Cop(6)
            newCop.create_cop()
            balls.append(newCop)
            target.generateNewCoord()
        elif score == 10 and len(balls) == 3:
            newCop = Cop(7)
            newCop.create_cop()
            balls.append(newCop)
            target.generateNewCoord()
        elif score == 15 and len(balls) == 4:
            newCop = Cop(8)
            newCop.create_cop()
            balls.append(newCop)
            target.generateNewCoord()
        elif score == 20 and len(balls) == 5:
            newCop = Cop(9)
            newCop.create_cop()
            balls.append(newCop)
            target.generateNewCoord()
        target.draw()
        thief.draw()
        displayScore()
        pygame.display.update()
        clock.tick(60)


gameLoop()
