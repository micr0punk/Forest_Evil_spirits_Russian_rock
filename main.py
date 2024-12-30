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
    def __init__(self, width, height, screen, screen_width, screen_height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 32
        self.mas = [[0] * width for _ in range(height)]

        self.grass_image = load_image("grass_image.png")
        self.border_image = load_image("border_image.png")
        self.mage_image = load_image("mage_texture2.png")

        self.where_x, self.where_y = 62, 90

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        cs = self.cell_size
        for y in range(self.height):
            for x in range(self.width):
                if (0 <= x <= 1 or 0 <= y <= 1 or self.width - 2 <= x <= self.width - 1 or
                        self.height - 2 <= y <= self.height - 1):
                    pygame.draw.rect(screen, pygame.Color('white'), (x * cs + self.left, y * cs + self.top, cs, cs))
                    screen.blit(self.border_image, (x * cs + self.left, y * cs + self.top))
                else:
                    pygame.draw.rect(screen, pygame.Color('white'), (x * cs + self.left, y * cs + self.top, cs, cs))
                    screen.blit(self.grass_image, (x * cs + self.left, y * cs + self.top))

        screen.blit(self.mage_image, (self.where_x, self.where_y))

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
    xr = xl = yu = yd = False
    #  test_hero = load_image("mage_texture.png")

    width = 26
    height = 12
    left = 62
    top = 90
    cell_size = 64

    size = width_ww, height_ww = 1820, 980

    screen = pygame.display.set_mode(size)

    board = Board(width, height, screen, width_ww, height_ww)
    board.set_view(left, top, cell_size)

    pygame.display.set_caption('Лес. Нечисть. Русский рок.')

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    yu = True
                if event.key == pygame.K_DOWN:
                    yd = True
                if event.key == pygame.K_RIGHT:
                    xr = True
                if event.key == pygame.K_LEFT:
                    xl = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    yu = False
                if event.key == pygame.K_DOWN:
                    yd = False
                if event.key == pygame.K_RIGHT:
                    xr = False
                if event.key == pygame.K_LEFT:
                    xl = False

        if xr:
            board.where_x += 64
            xr = False
        elif xl:
            board.where_x -= 64
            xl = False
        elif yu:
            board.where_y -= 64
            yu = False
        elif yd:
            board.where_y += 64
            yd = False

        screen.fill((0, 0, 0))
        board.render(screen)

        pygame.display.flip()


if __name__ == '__main__':
    main()
