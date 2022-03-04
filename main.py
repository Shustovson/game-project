import pygame, controls
def run():

    pygame.init()
    bg_image = pygame.image.load('Images/Menu.jpg')
    screen = pygame.display.set_mode((1920,1080))
    pygame.display.set_caption("Забей")

    while True:
        controls.events(screen)  ###Прослушивание событий
        controls.update(bg_image, screen)  ###Отрисовка изображения


run()


