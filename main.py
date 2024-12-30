import pygame
import os
import sys

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)

    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()

    return image


class Board:
    def __init__(self, width, height, screen):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.mas = [[0] * width for _ in range(height)]
        self.grass_image = load_image("grass_image.png")

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        cs = self.cell_size
        for y in range(self.height):
            for x in range(self.width):
                if self.mas[y][x] == 1:
                    pygame.draw.rect(screen, pygame.Color('white'), (x * cs + self.left, y * cs + self.top, cs, cs))
                    screen.blit(self.grass_image, (x * cs + self.left, y * cs + self.top))
                else:
                    pygame.draw.rect(screen, pygame.Color('white'), (x * cs + self.left, y * cs + self.top, cs, cs), 1)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)

    def get_cell(self, mp):
        where_x, where_y = mp
        if self.left <= where_x <= self.left + self.cell_size * self.width and \
                self.top <= where_y <= self.top + self.cell_size * self.height:
            return where_x // self.cell_size - 2, where_y // self.cell_size - 2
        else:
            return None

    def is_in_table(self, mp):
        where_x, where_y = mp
        if self.left <= where_x <= self.left + self.cell_size * self.width and \
                self.top <= where_y <= self.top + self.cell_size * self.height:
            return True
        else:
            return False

    def update(self, mp):
        coords = self.get_cell(mp)
        if coords is not None:
            coords = list(self.get_cell(mp))
            xinst, yinst = coords[0], coords[1]
            for x in range(self.width):
                coords[0] = x
                state = self.mas[coords[1]][coords[0]]
                if self.is_in_table(mp):
                    if state == 0:
                        self.mas[coords[1]][coords[0]] = 1
                    else:
                        self.mas[coords[1]][coords[0]] = 0
            coords[0] = xinst
            for y in range(self.height):
                coords[1] = y
                state = self.mas[coords[1]][coords[0]]
                if self.is_in_table(mp):
                    if state == 0:
                        self.mas[coords[1]][coords[0]] = 1
                    elif state == 1 and not y == yinst:
                        self.mas[coords[1]][coords[0]] = 0


def main():
    pygame.init()
    running = True

    width = 5
    height = 7
    left = 100
    top = 100
    cell_size = 50

    size = width_ww, height_ww = 450, 550
    screen = pygame.display.set_mode(size)

    board = Board(width, height, screen)
    board.set_view(left, top, cell_size)

    pygame.display.set_caption('Лес. Нечисть. Русский рок.')

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
                board.update(event.pos)

        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
