import pygame, time
import data.engine as e
from settings import *
from pygame.locals import *


class MenuScreen:
    def __init__(self, screen, clock, smallFont, largeFont, background):
        self.clock = clock
        self.screen = screen
        self.smallFont = smallFont
        self.largeFont = largeFont
        self.showFPS = True
        self.fullscreen = False
        self.background = e.entity(0, 0, 640, 480, background)
        self.button = pygame.image.load('data/images/button01.png').convert_alpha()
        self.selectedButton = pygame.image.load('data/images/buttonPressed01.png').convert_alpha()
        self.unavailableButton = pygame.image.load('data/images/unavailableButton.png').convert_alpha()
        self.unavailableSelected = pygame.image.load('data/images/unavailableSelected.png').convert_alpha()
        # стартуем отрисовку меню, показываем его, пока running верно

    def start(self, showFPS):
        self.showFPS = showFPS
        self.running = True
        while self.running:
            self.start_time = time.time()
            self.draw()  # рисуем
            self.events()  # проверяем ивенты меню
            self.update()  # обновляем
        #

    def draw(self):
        self.background.display(self.screen, [0, 0])
        self.background.changeFrame(1)
        self.largeFont.render(self.screen, self.title, (40, 120), WHITE)

    def events(self):
        pass

    def update(self):
        pass

    def fillArray(self, array):
        for x in range(len(array)):
            array[x] = False
        return array


class MainMenu(MenuScreen):
    def __init__(self, screen, clock, smallFont, largeFont, background):
        super().__init__(screen, clock, smallFont, largeFont, background)
        self.options = OptionsMenu(self.screen, self.clock, self.smallFont, self.largeFont, 'menuBackground')
        self.stateList = [True]
        self.buttonList = []
        self.title = ''




    # обновляем, если нажата клавиша
    def update(self):
        y = 180
        i = 0
        for state in self.stateList:
                if i == 1:
                    if not self.progress:
                        self.screen.blit(self.unavailableButton, (40, y))
                    else:
                        self.screen.blit(self.button, (40, y))
                pygame.display.update()


class VideoMenu(MenuScreen):
    def __init__(self):
        super().__init__()


class OptionsMenu(MenuScreen):
    # инциализация
    def __init__(self, screen, clock, smallFont, largeFont, background):
        super().__init__(screen, clock, smallFont, largeFont, background)
        self.stateList = [True, False, False]
        self.buttonList = ['Video', 'Controls', 'Back']
        self.descriptions = ['Video options',
                             'See controls in game',
                             'Go back to Main Menu']
        self.title = 'Options'

    # когда нажимаем на клавишу идет проверка
    def events(self):
        self.running = e.checkCloseButtons()
        index = self.stateList.index(True)
        for event in pygame.event.get():
            self.running, self.fullscreen, self.screen = e.checkEvents(event, self.running, self.fullscreen, self.screen)
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if index == 0:
                        self.video.start(self.showFPS)
                    elif index == 1:
                        pass
                    elif index == 2:
                        self.running = False
                if event.key == K_DOWN:
                    if index < len(self.stateList) - 1:
                        self.stateList[index] = False
                        self.stateList[index + 1] = True
                if event.key == K_UP:
                    if index != 0:
                        self.stateList[index] = False
                        self.stateList[index - 1] = True
                elif event.key == K_ESCAPE:
                    self.running = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if pos[0] >= 44 and pos[0] <= 174:
                    if pos[1] >= 187 and pos[1] <= 216:
                        self.video.start(self.showFPS)
                    elif pos[1] >= 228 and pos[1] <= 261:
                        pass
                    elif pos[1] >= 271 and pos[1] <= 301:
                        self.running = False
    # обновляем
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
        y = 180
        i = 0
        for state in self.stateList:
            if state:
                self.screen.blit(self.selectedButton, (40, y))
                self.smallFont.render(self.screen, self.descriptions[i],
                                      (200, y + 12), WHITE)
            else:
                self.screen.blit(self.button, (40, y))
            self.smallFont.render(self.screen, self.buttonList[i],
                                  (65, y + 12), WHITE)
            y += 43
            i += 1
        self.showFPS = self.video.showFPS
        if self.showFPS:
            fps = str(int(1.0 / (time.time() - self.start_time)))
            self.smallFont.render(self.screen, fps, (WIDTH - 40, 20))
        pygame.display.update()
        self.clock.tick(FPS)
