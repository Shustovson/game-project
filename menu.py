import pygame
import data.engine as e


class MenuScreen:
    def __init__(self, screen, clock, smallFont, largeFont, background):
        self.clock = clock
        self.screen = screen
        self.smallFont = smallFont
        self.largeFont = largeFont
        self.showFPS = False
        self.fullscreen = False
        self.background = e.entity(0, 0, 640, 480, background)
    # стартуем отрисовку меню, показываем его, пока running верно
    def start(self, showFPS):
        self.showFPS = showFPS
        self.running = True
        while self.running:
            self.draw()
            self.update()
    #
    def draw(self):
        self.background.display(self.screen, [0, 0])



    def update(self):
        pass



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


class OptionsMenu(MenuScreen):
    def update(self):
        pygame.display.update()
