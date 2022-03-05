import pygame, controls


class Button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text


    def draw(self, screen, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 2)

        if self.text != '':
            font = pygame.font.Font('Font\Defect.otf', 55)  # Размер шрифта
            text = font.render(self.text, 1, (255, 255, 255))  # Цвет букв в главном меню
            screen.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


def MenuWindow(screen):
    #win.fill((0, 180, 210)) - одноцветный фон
    Start_BT = Button((0, 255, 0), 1500, 500, 250, 70, "Начать игру")
    Options_BT = Button((255, 255, 255), 1500, 600, 250, 70, "Опции")
    Exit_BT = Button((255, 255, 255), 1500, 800, 250, 70, "Выход")
    Achievements_BT = Button((255, 255, 255), 1500, 700, 250, 70, "Достижения")
    Start_BT.draw(screen, (0, 0, 0))
    Options_BT.draw(screen, (0, 0, 0))
    Exit_BT.draw(screen, (0, 0, 0))
    Achievements_BT.draw(screen, (0, 0, 0))