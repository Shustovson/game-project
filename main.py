import pygame, controls

import Menu_Buttons


def run():

    pygame.init()
    bg_image = pygame.image.load('Images/Menu.jpg')
    bg_image_rect = bg_image.get_rect(
        bottomright = (1920,1080)
    )
    screen = pygame.display.set_mode((1920,1080))
    pygame.display.set_caption("Забей")
    screen.blit(bg_image, bg_image_rect)
    pygame.mixer.music.load("Music/Trec1.mp3")
    pygame.mixer.music.play(-1)

    while True:
        controls.events()  ###Прослушивание событий
        controls.update(bg_image, screen)  ###Отрисовка изображения
        Menu_Buttons.MenuWindow(screen)


run()



