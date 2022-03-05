import pygame, sys
from Menu_Buttons import Button


def events():
    for event in pygame.event.get():  ###Получаем все события пользователя
        if event.type == pygame.QUIT:
            sys.exit()  ###Если пользователь выходит из игры, то игра закрывается

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()

def update(bg_image, screen):###Отрисовка всего экрана

    pygame.display.flip()  ###Прорисовка последнего экрана
