import pygame, sys

def events():
    for event in pygame.event.get():  ###Получаем все события пользователя
        if event.type == pygame.QUIT:
            sys.exit()  ###Если пользователь выходит из игры, то игра закрывается

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()

def update(bg_image, screen):###Отрисовка всего экрана

    pygame.display.flip()  ###Прорисовка последнего экрана
    start_button = pygame.draw.rect(screen, (255, 255, 255), (1600, 600, 180, 50));
    continue_button = pygame.draw.rect(screen, (255, 255, 255), (1600,670, 180, 50));
    quit_button = pygame.draw.rect(screen, (255, 255, 255), (1600, 740 , 180, 50));
