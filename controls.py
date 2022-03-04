import pygame, sys

def events(screen):
    for event in pygame.event.get():  ###Получаем все события пользователя
        if event.type == pygame.QUIT:
            sys.exit()  ###Если пользователь выходит из игры, то игра закрывается

def update(bg_image, screen):###Отрисовка всего экрана
    screen.fill(bg_image)  ###Устанавливаем цвет заднего фона
    pygame.display.flip()  ###Прорисовка последнего экрана