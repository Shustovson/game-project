import pygame, sys, os, time, numpy  # подключаю используемые библиотеки
from settings import *
import data.engine as e
from Player import Player

# класс карты
class MapObject:
    # инициализация карты
    def __init__(self, screen, x, y, xSize, ySize, type):
        self.entity = e.entity(x, y, xSize, ySize, type)
        self.screen = screen
        self.type = type
    # обновление карты при скролле и при обновлении кадров
    def update(self, scroll):
        self.entity.changeFrame(1)
        self.entity.display(self.screen, scroll)
 # класс двигающейся платформы
class MovingPlatform(MapObject):
    # опять инициализируем
    def __init__(self, screen, x, y, xSize, ySize, type, maxAxis, speed):
        super().__init__(screen, x, y, xSize, ySize, type)
        self.movement = [x,y] # координаты платормы
        self.forward = True # направлеие
        self.speed = speed # скорость
        if self.type == "horizontal": # определеяем где начало и конец в зависимости от типа
            self.maxAxis = x + maxAxis
            self.minAxis = x - maxAxis
        else:
            self.maxAxis = y + maxAxis
            self.minAxis = y - maxAxis
    # обновляем платформу
    def update(self, scroll):
        distance = 0
        # если горизонтальна
        if self.type == "horizontal":
            if self.movement[0] >= self.maxAxis or self.movement[0] <= self.minAxis:
                self.forward = not self.forward # меняем направление движения
            if self.forward:
                self.movement[0] += self.speed # двигаем платформу на единицу её скорости
                distance = self.speed
            else:
                self.movement[0] -= self.speed # двигаем платформу обратно
                distance = - self.speed
        else:
            if self.movement[1] >= self.maxAxis or self.movement[1] <= self.minAxis:
                self.forward = not self.forward
            if self.forward:
                self.movement[1] += self.speed
            else:
                self.movement[1] -= self.speed
        if self.entity.obj.x <= 0:
            self.entity.obj.x = 0 # устанавливаем ноль, если платформа слишком быстро двигалась и ушла за ноль
        self.entity.set_pos(self.movement[0], self.movement[1])
        # обновляем кадры и рисуем
        self.entity.changeFrame(1)
        self.entity.display(self.screen, scroll)

        return distance
 # неподвижная платформа
class StaticPlatform(MapObject):
    # инициализация
    def __init__(self, screen, x, y, xSize, ySize, type):
        super().__init__(screen, x, y, xSize, ySize, type)
        self.entity.obj.x = x
        self.entity.obj.y = y
    # обновление
    def update(self, scroll):
        self.entity.changeFrame(1)
        self.entity.display(self.screen, scroll)

        return MOVING_SPEED


# задаем карту и изображения из которых она собирается
class MapLevel:
    def __init__(self, screen, x, y, map, speed):
        self.screen = screen
        # загрузим изображения
        self.layer00 = e.loadImage('data/images/background40.png', alpha=True)
        self.layer01 = e.loadImage('data/images/background41.png', alpha=True)
        self.layer02 = e.loadImage('data/images/background42.png', alpha=True)
        self.layerList = [self.layer00, self.layer01, self.layer02]

        self.leftPlat = e.loadImage('data/images/plat07.png')
        self.rightPlat = e.loadImage('data/images/plat10.png')
        self.middlePlat00 = e.loadImage('data/images/plat08.png')
        self.middlePlat01 = e.loadImage('data/images/plat09.png')
        self.middlePlat02 = e.loadImage('data/images/plat06.png')
        self.middlePlat03 = e.loadImage('data/images/plat11.png', alpha=True)

        self.cornerPlat00 = e.loadImage('data/images/plat24.png', alpha=True)
        self.cornerPlat01 = e.loadImage('data/images/plat25.png', alpha=True)

        self.barrelBottom = e.loadImage('data/images/barrelBottom.png', alpha=True)
        self.barrelTop = e.loadImage('data/images/barrelTop.png', alpha=True)
        self.cable00 = e.loadImage('data/images/deco00.png', alpha=True)
        self.cable01 = e.loadImage('data/images/deco01.png', alpha=True)
        self.cable02 = e.loadImage('data/images/deco02.png', alpha=True)
        self.chainBottom = e.loadImage('data/images/chainBottom.png', alpha=True)
        self.chain = e.loadImage('data/images/chain.png', alpha=True)

        self.spikes = e.loadImage('data/images/chainBottom.png', alpha=True)

        self.static = e.loadImage('data/images/plat12.png', alpha=True)
        self.gameMap = e.load_map('data/' + map)
        #  добавим игрока
        self.player = Player(x, y)
        self.playerX = x
        self.playerY = y
        self.movingList = []
        self.enemiesList = []
        self.notCollisionable = []
        self.trueScroll = [0, 0]
        self.create = True
        self.backgroundSpeed = speed

    # функция отрисовки, работает в зависимости от переданного временного шага
    def draw(self, dt):
        self.screen.fill(BEIGE)
        # слежка отображаемого контента за движениями игрока
        self.trueScroll[0] += (self.player.entity.x -
                               self.trueScroll[0] - (WIDTH / 2)) / 20
        self.trueScroll[1] += (self.player.entity.y -
                               self.trueScroll[1] - (HEIGHT / 2)) / 20

        self.scroll = self.trueScroll.copy()
        self.scroll[0] = int(self.scroll[0])
        self.scroll[1] = int(self.scroll[1])

        # отрисовываем раннее загруженный бэк изображений
        i = 0
        for layer in self.layerList:
            self.screen.blit(layer, (-100 - self.scroll[0] * self.backgroundSpeed[i],
                                     -80 - (self.scroll[1] / 1) * self.backgroundSpeed[i]))
            i += 1

        self.tile_rects = []
        self.jumpRects = []
        self.platRects = []
        # отрисовываем карту из файла карты, карта это текстовый файл, где каждый символ отвечает за определенную плитку
        y = 0
        for layer in self.gameMap:
            x = 0
            for tile in layer:
                if x >= 0 and x <= WIDTH and y >= 0 and y <= HEIGHT:
                    if self.create:
                        if tile == '1':
                            plat = StaticPlatform(self.screen, x * TILE_SIZE, y * TILE_SIZE, 64, 32, 'static')
                            self.movingList.append(plat)
                        elif tile == '2':
                            plat = MovingPlatform(self.screen, x * TILE_SIZE, y * TILE_SIZE, 64, 32, 'vertical', 90, 3)
                            self.movingList.append(plat)
                        elif tile == '3':
                            plat = MovingPlatform(self.screen, x * TILE_SIZE, y * TILE_SIZE, 64, 32, 'horizontal', 90,
                                                  3.5)
                            self.movingList.append(plat)
                        elif tile == 'b':
                            enemy = MapObject(self.screen, x * TILE_SIZE, y * TILE_SIZE + 16, 32, 16, 'spikeTop')
                            self.enemiesList.append(enemy)
                        elif tile == 'k':
                            plat = MapObject(self.screen, x * TILE_SIZE, y * TILE_SIZE, 32, 16, 'throughMiddle')
                            self.movingList.append(plat)
                        elif tile == 'l':
                            plat = MapObject(self.screen, x * TILE_SIZE, y * TILE_SIZE, 32, 16, 'throughLeft')
                            self.movingList.append(plat)
                        elif tile == 'm':
                            plat = MapObject(self.screen, x * TILE_SIZE, y * TILE_SIZE, 32, 16, 'throughRight')
                            self.movingList.append(plat)
                        elif tile == 'n':
                            plat = MapObject(self.screen, x * TILE_SIZE, y * TILE_SIZE, 64, 64, 'endBall')
                            self.notCollisionable.append(plat)
                    elif tile == '7':
                        e.displayTile(self.middlePlat02, self.screen, self.scroll, x, y)
                    elif tile == '4':
                        e.displayTile(self.leftPlat, self.screen, self.scroll, x, y)
                    elif tile == '5':
                        e.displayTile(self.middlePlat00, self.screen, self.scroll, x, y)
                    elif tile == '6':
                        e.displayTile(self.middlePlat01, self.screen, self.scroll, x, y)
                    elif tile == '8':
                        e.displayTile(self.rightPlat, self.screen, self.scroll, x, y)
                    elif tile == '9':
                        e.displayTile(self.cornerPlat00, self.screen, self.scroll, x, y)
                    elif tile == 'a':
                        e.displayTile(self.cornerPlat01, self.screen, self.scroll, x, y)
                    elif tile == 'c':
                        e.displayTile(self.barrelBottom, self.screen, self.scroll, x, y)
                    elif tile == 'd':
                        e.displayTile(self.barrelTop, self.screen, self.scroll, x, y)
                    elif tile == 'e':
                        e.displayTile(self.chain, self.screen, self.scroll, x, y)
                    elif tile == 'f':
                        e.displayTile(self.chainBottom, self.screen, self.scroll, x, y)
                    elif tile == 'g':
                        e.displayTile(self.cable00, self.screen, self.scroll, x, y)
                    elif tile == 'h':
                        e.displayTile(self.cable01, self.screen, self.scroll, x, y)
                    elif tile == 'i':
                        e.displayTile(self.cable02, self.screen, self.scroll, x, y)
                    elif tile == 'j':
                        e.displayTile(self.middlePlat03, self.screen, self.scroll, x, y)
                    if tile not in ['0', '1', '2', '3', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n']:
                        self.tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                x += 1
            y += 1
        self.create = False

    # выполняем библиотечное событие по вызову, на случай
    def events(self, event, dt):
        self.player.events(event, dt)

    # обновляем карту
    def update(self, dt):
        distance = 0
        levelIsOver = False
        for platform in self.movingList:
            distance = platform.update(self.scroll)
        for platform in self.notCollisionable:
            platform.update(self.scroll)
        for enemy in self.enemiesList:
            enemy.update(self.scroll)
        levelData = self.player.update(self.tile_rects, self.enemiesList, self.movingList, self.notCollisionable,
                                       self.screen, self.scroll, dt, distance)
        if levelData[0]:  # restart level
            self.restart()
        if levelData[1]:  # level is over, go to next level
            levelIsOver = True

        return [self.player.entity.obj.x,
                self.player.entity.obj.y], self.player.airTimer, self.player.momentum, self.scroll, levelIsOver

    # рестарт игры, отправлем игрока на начало
    def restart(self):
        self.player = Player(self.playerX, self.playerY)

    # рестарт переменных, которые следят за игроком
    def restartVariables(self, pos):
        self.player.movingRight = False
        self.player.movingLeft = False
        self.player.momentum = 0
        self.player.airTimer = 0
        self.player.movement = [0, 0]
        self.player.entity.set_pos(pos[0], pos[1])