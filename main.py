import pygame


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.mas = [[0] * width for _ in range(height)]

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
    width = 5
    height = 7
    board = Board(width, height)
    running = True
    size = width_ww, height_ww = 450, 550
    left = 100
    top = 100
    cell_size = 50
    board.set_view(left, top, cell_size)
    pygame.display.set_caption('Чёрное в белое и наоборот')
    screen = pygame.display.set_mode(size)
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
