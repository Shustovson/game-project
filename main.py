import pygame
import data.engine as e
from settings import *
from menu import MainMenu


class Core:
    def __init__(self):
        pygame.init()
        pygame.mixer.pre_init(44100, -16, 2, 512)
        self.screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
        self.clock = pygame.time.Clock()
        icon = e.loadImage('data/images/chain.png', alpha=True)
        e.load_animations('data/images/entities/')
        self.smallFont = e.Font('data/images/small_font2.png')
        self.largeFont = e.Font('data/images/large_font.png')
        pygame.display.set_icon(icon)
        pygame.display.set_caption('NOT A game')
        self.running = True
        self.showFPS = True
    # создаем окно
    def new(self):
        self.menu = MainMenu(self.screen,  self.clock, self.smallFont, self.largeFont, 'menuBackground')
        self.run()
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