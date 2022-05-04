import pygame, sys, os, time, numpy # подключаю используемые библиотеки, важно установить pygame
from pygame.locals import *
from Objects import *
from menu import MenuScreen, OptionsMenu

# класс игры
class Game:
    # инициализация по переданным параметрам
    def __init__(self, screen, clock, smallFont, largeFont, index):

        self.screen = screen
        self.clock = clock
        self.smallFont = smallFont
        self.largeFont = largeFont
        self.pause = Pause(self.screen)
        self.levelList = [MapLevel(self.screen, 50, 200, 'map01', FAST_SPEED),
                          MapLevel(self.screen, 140, 0, 'map02', NORMAL_SPEED)]
        self.running = True
        self.isPaused = False
        self.fullscreen = False
        self.restart = False
        self.levelIndex = index
        self.screen.set_alpha(None)
        # библиотечный прием для отрисовки с определенной частотой кадров
        self.startTime: int = 0
        self.inverseFPS: float = 1 / FPS
        self.dt: float = self.inverseFPS
        self.timeElapsed: int = 0
        self.delay: float = 1000 / FPS
        self.currentFPS: int = FPS
        self.fpsCounter: list = [0, 0]
    #
    def start(self, showFPS):
        self.showFPS = showFPS
        while self.running:
            self.startTime: int = pygame.time.get_ticks()
            self.fpsCounter[0] += self.timeElapsed
            self.fpsCounter[1] += self.delay
            if self.fpsCounter[1] >= 1000:
                if self.fpsCounter[0] > 0:
                    self.currentFPS = str(int((self.fpsCounter[1] / self.fpsCounter[0]) * FPS))
                else:
                    self.currentFPS = "MAX"
                self.fpsCounter = [0, 0]
            self.draw()
            self.events()
            pygame.event.pump()
            self.update()
            self.timeElapsed = pygame.time.get_ticks() - self.startTime
            self.dt = max(self.inverseFPS, self.timeElapsed / 1000)
            pygame.time.delay(max(0, int(self.delay - self.timeElapsed)))
    # отрисовываем игру
    def draw(self):
        self.levelList[self.levelIndex].draw(self.dt)
    # проверка событий
    def events(self):
        # проверяем на закрытие
        self.running = e.checkCloseButtons()
        # проверяем на закрытие, рестарт и обновляем игру
        for event in pygame.event.get():
            self.levelList[self.levelIndex].events(event, self.dt)
            self.running, self.fullscreen, self.screen = e.checkEvents(event, self.running, self.fullscreen, self.screen)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    quit('Game Closed by User')
                if event.key == K_p:
                    self.isPaused = not self.isPaused
                if event.key == K_RETURN:
                    self.restart = True
    # обновляем экран игры, проверяем нажали ли паузу или рестарт
    def update(self):
        movement, airTimer, momentum, scroll, levelIsOver = self.levelList[self.levelIndex].update(self.dt)
        # если нажали на паузу
        if self.isPaused:
            pos = [self.levelList[self.levelIndex].player.entity.x, self.levelList[self.levelIndex].player.entity.y]
            self.levelList[self.levelIndex].restartVariables(pos)
            screenshot = self.screen.copy()
            self.pause.start(screenshot)
            self.isPaused = not self.isPaused
        # если нажали рестар
        if self.restart:
            self.levelList[self.levelIndex].restart()
            self.restart = False
        # если уровень закончен
        if levelIsOver:
            self.levelIndex += 1
            file = open('data/saver.txt', 'w')
            file.write(str(self.levelIndex))
            file.close()
        # если вышли за границы карты
        if movement[1] >= 1200:
            self.restart = True
        # если хотим видеть фпс рендерим его
        if self.showFPS :
            self.smallFont.render(self.screen, str(self.currentFPS), (WIDTH - 40, 20), RED)
        self.smallFont.render(self.screen, "movement: " + str(int(movement[0])) + ", " +
                                    str(int(movement[1])), (20, 20), WHITE)
        self.smallFont.render(self.screen, "air timer: " + str(airTimer), (20, 40), WHITE)
        self.smallFont.render(self.screen, "momentum: " + str(int(momentum)), (20, 60), WHITE)
        self.smallFont.render(self.screen, "scroll: " + str(int(scroll[0])) + ", " +
                                    str(int(scroll[1])), (20, 80), WHITE)
        pygame.display.update() # обновляем экран

# класс экрана меню

# класс паузы
class Pause:
    # инициализируем его
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load('data/images/pauseBackground.png').convert_alpha()
        self.fullscreen = False
    # запускаем
    def start(self, screenshot):
        self.running = True
        screenshot = e.blurSurf(screenshot, 4.5)
        while self.running:
            self.draw(screenshot)
            self.events()
            self.update()
    # отрисовываем
    def draw(self, screenshot):
        self.screen.blit(screenshot, (0, 0))
        self.screen.blit(self.background, (0, 0))
    # проверка на нажатие клавиш
    def events(self):
        self.running = e.checkCloseButtons()

        for event in pygame.event.get():
            self.running, self.fullscreen, self.screen = e.checkEvents(event, self.running, self.fullscreen, self.screen)
            if event.type == KEYDOWN:
                if event.key == K_p:
                    self.running = False
                    if event.key == K_ESCAPE:
                        exit("Game Closed")

    def update(self):
        pygame.display.update()
# задаем окно и ключевые данные для работы в отдельном окне
# класс основного, начального меню
class MainMenu(MenuScreen):
    def __init__(self, screen, clock, smallFont, largeFont, background):
        super().__init__(screen, clock, smallFont, largeFont, background)
        self.options = OptionsMenu(self.screen, self.clock, self.smallFont, self.largeFont, 'menuBackground')
        self.stateList = [True, False, False, False, False]
        self.buttonList = ['Start', 'Continue', 'Options', 'About', 'Quit']
        self.descriptions = ['Start new game',
                             'Continue where you left',
                             'Explore game options',
                             'About this game',
                             'Exit to desktop']
        self.title = 'Main Menu'
        self.showFPS = True
        self.screenshot = None
        self.progress = False
        if os.stat('data/saver.txt').st_size != 0:
            self.progress = True
            with open('data/saver.txt') as file:
                index = int(file.readline().strip())
        else:
            index = 0
        self.game = Game(self.screen, self.clock, self.smallFont, self.largeFont, index)

    # проверяе нажатие на кнопки
    def events(self):
        self.running = e.checkCloseButtons()
        index = self.stateList.index(True)
        for event in pygame.event.get():
            self.running, self.fullscreen, self.screen = e.checkEvents(event, self.running, self.fullscreen, self.screen)
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if index == 0:
                        fade(640, 480, self.screenshot, self.screen)
                        self.game = Game(self.screen, self.clock, self.smallFont, self.largeFont, 0)
                        self.game.start(self.showFPS)
                    elif index == 1:
                        if self.progress:
                            self.game.start(self.showFPS)
                    elif index == 2:
                        self.options.start(self.showFPS)
                    elif index == 3:
                        pass
                    elif index == 4:
                        self.running = False
                if event.key == K_DOWN:
                    if index < len(self.stateList) - 1:
                        self.stateList[index] = False
                        self.stateList[index + 1] = True
                if event.key == K_UP:
                    if index != 0:
                        self.stateList[index] = False
                        self.stateList[index - 1] = True
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if pos[0] >= 44 and pos[0] <= 174:
                    if pos[1] >= 187 and pos[1] <= 216:
                        self.game.start(self.showFPS)
                    elif pos[1] >= 228 and pos[1] <= 261:
                        if self.progress:
                            self.game.start(self.showFPS)
                    elif pos[1] >= 271 and pos[1] <= 301:
                        self.options.start(self.showFPS)
                    elif pos[1] >= 314 and pos[1] <= 346:
                        pass
                    elif pos[1] >= 357 and pos[1] <= 386:
                        self.running = False
    # обновляем, если нажата клавиша
    def update(self):
        pos = pygame.mouse.get_pos()
        if pos[0] >= 44 and pos[0] <= 174:
            if pos[1] >= 187 and pos[1] <= 216:
                self.stateList = self.fillArray(self.stateList)
                self.stateList[0] = True
            elif pos[1] >= 228 and pos[1] <= 261:
                self.stateList = self.fillArray(self.stateList)
                self.stateList[1] = True
            elif pos[1] >= 271 and pos[1] <= 301:
                self.stateList = self.fillArray(self.stateList)
                self.stateList[2] = True
            elif pos[1] >= 314 and pos[1] <= 346:
                self.stateList = self.fillArray(self.stateList)
                self.stateList[3] = True
            elif pos[1] >= 357 and pos[1] <= 386:
                self.stateList = self.fillArray(self.stateList)
                self.stateList[4] = True
        y = 180
        i = 0
        for state in self.stateList:
            if state:
                if i == 1:
                    if not self.progress:
                        self.screen.blit(self.unavailableSelected, (40, y))
                    else:
                        self.screen.blit(self.selectedButton, (40, y))
                else:
                    self.screen.blit(self.selectedButton, (40, y))
                self.smallFont.render(self.screen, self.descriptions[i],
                                      (200, y + 14), WHITE)
                self.smallFont.render(self.screen, self.buttonList[i],
                                     (65, y + 14), WHITE)
            else:
                if i == 1:
                    if not self.progress:
                        self.screen.blit(self.unavailableButton, (40, y))
                    else:
                        self.screen.blit(self.button, (40, y))
                else:
                    self.screen.blit(self.button, (40, y))
                self.smallFont.render(self.screen, self.buttonList[i],
                                        (65, y + 10), WHITE)
            y += 43
            i += 1
        self.showFPS = self.options.showFPS
        if self.showFPS:
            fps = str(int(1.0 / (time.time() - self.start_time)))
            self.smallFont.render(self.screen, fps, (WIDTH - 40, 20))
        self.screenshot = self.screen.copy()
        pygame.display.update()
        self.clock.tick(FPS)
class Core:
    def __init__(self):
        # задаем окно
        pygame.init()
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.set_num_channels(64)
        pygame.display.set_caption('APieceWeFall')
        self.screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
        self.clock = pygame.time.Clock()
        # иконка
        icon = e.loadImage('data/images/chain.png', alpha=True)
        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP]) # клавишы которые будет читать программа
        e.load_animations('data/images/entities/') # загрузим анимации
        self.smallFont = e.Font('data/images/small_font2.png')# загрузим шрифты
        self.largeFont = e.Font('data/images/large_font.png')
        pygame.display.set_icon(icon) # устанавливаем иконку
        self.running = True # запускаем
        self.showFPS = True # отображаем фпс
    # создаем окно
    def new(self):
        self.menu = MainMenu(self.screen,  self.clock, self.smallFont, self.largeFont, 'menuBackground')
        self.run()
    # запускаем
    def run(self):
        self.menu.start(self.showFPS)
        self.running = self.menu.running

# добавляем затемнение для паузы
def fade(width, height, screenshot, screen):
    fade = pygame.Surface((width, height))
    fade.fill((0,0,0))
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        screen.blit(screenshot, (0, 0))
        screen.blit(fade, (0,0))
        pygame.display.update()

c = Core()
while c.running:
    c.new()
pygame.quit()