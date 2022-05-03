import pygame, sys, os, time, numpy # подключаю используемые библиотеки
import data.engine as e
from pygame.locals import *

# класс игрока
class Player:
    # инициализация игрока
    def __init__(self, x, y):
        self.entity = e.entity(x, y, 32, 32, 'player')
        self.movingRight = False # движется ли направо
        self.movingLeft = False # движителся ли налево
        self.momentum = 0 # момент
        self.airTimer = 0 # время в воздухе
        self.movement = [0,0] # координаты движения
        self.platformCollision = False # скольжение по платорме
        self.onPlatform = False # находится ли на платформе
        self.through = False # прохождение сквозь
        self.levelOver = False
    # события клавиш
    def events(self, event, dt):
        # изменяем состояние объекта, если клавиша нажата
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                self.movingRight = True
            if event.key == K_d:
                self.movingRight = True
            if event.key == K_LEFT:
                self.movingLeft = True
            if event.key == K_a:
                self.movingLeft = True
            if event.key == K_UP:
                if self.airTimer == 0:
                    self.momentum = -5
            if event.key == K_w:
                if self.airTimer == 0:
                    self.momentum = -5
            if event.key == K_DOWN:
                self.through = not self.through
            if event.key == K_s:
                self.through = not self.through
        # изменяем состояния если клавишу отпустили
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                self.movingRight = False
            if event.key == K_d:
                self.movingRight = False
            if event.key == K_LEFT:
                self.movingLeft = False
            if event.key == K_a:
                self.movingLeft = False
            if event.key == K_DOWN:
                self.through = not self.through
            if event.key == K_s:
                self.through = not self.through
    # обновление состояния
    def update(self, tile_rects, enemiesList, movingList, notCollisionable, screen, scroll, dt, distance):
        self.movement = [0,0]
        # если состояние движение активировано, то координаты меняютя
        if self.movingRight == True:
            self.movement[0] += 300 * dt
        if self.movingLeft == True:
            self.movement[0] -= 300 * dt
        # изменяю момент, чтобы движение не было линейным
        self.movement[1] += self.momentum * 2.4
        self.momentum += 22 * dt
        if self.momentum > 5:
            self.momentum = 5
        # меняем состояние для отрисовки движения
        if self.movement[0] == 0:
            self.entity.set_action('idle')
        elif self.movement[0] > 0:
            self.entity.set_flip(False)
            self.entity.set_action('run')
        elif self.movement[0] < 0:
            self.entity.set_flip(True)
            self.entity.set_action('run')
        if self.airTimer != 0:
            self.entity.set_action('jump')

        collisionList = self.entity.move(self.movement, tile_rects, enemiesList, movingList, notCollisionable, self.airTimer, self.through)

        exitData = [False, False]
        # проходим по платформам
        for platform in collisionList['data']:
            if platform[1][3]:
                self.airTimer = 0
                self.momentum = 0
                self.platformCollision = False
            else:
                self.airTimer = 0
                self.platformCollision = False
            # проверка на вертикальую платформу
            if platform[2] == 'horizontal':
                self.entity.obj.x += distance
            if platform[2] == "static":
                self.onPlatform = True
            if platform[2] == 'throughMiddle':
                pass
            else:
                self.onPlatform = False
            # выходим если наступили на колючки
            if platform[2] == "spikeTop":
                exitData[0] = True
            if platform[2] == "endBall":
                self.levelOver = True
                exitData[1] = True

        if not collisionList['bottom']:
            self.airTimer += 1
        # меняем кадр, проматываем экран
        self.entity.changeFrame(1)
        self.entity.display(screen, scroll)
        return exitData