import pygame
import os
import sys
import csv
from random import choice
from pathlib import Path


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

        # self.board = [[0] * width for _ in range(height)]
        self.room = [[0] * width for _ in range(height)]
        self.objects = [[0] * width for _ in range(height)]
        self.player = [[0] * width for _ in range(height)]
        self.player[height // 2][width // 2] = '5'
        self.current_room_y,  self.current_room_x = 6, 13

        self.left = 10
        self.top = 10
        self.cell_size = 32

        self.map_number = 1

        self.grass_image = load_image("grass_image.png")
        self.border_image = load_image("border_image.png")
        self.mage_image = load_image("mage_texture2.png")
        self.boulder_image = load_image("boulder_image.png")
        self.forest_exit_image = load_image("forest_exit.png")

        self.where_x, self.where_y = 46 + 64, 90 + 64

        self.roomsfolder = Path('rooms')
        self.number_of_rooms = len(list(self.roomsfolder.iterdir()))

        self.objectmapsfolder = Path('objectmaps')
        self.number_of_objectmaps = len(list(self.objectmapsfolder.iterdir()))
        self.pool_of_objectmaps = [x for x in range(1, self.number_of_objectmaps + 1)]

        self.levelmapsfolder = Path('levelmaps')
        self.number_of_levelmaps = len(list(self.levelmapsfolder.iterdir()))
        self.pool_of_levelmaps = [x for x in range(1, self.number_of_levelmaps + 1)]
        self.currentlevel = choice(self.pool_of_levelmaps)


    def return_player_coords(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.player[y][x] == '5':
                    return y, x

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        cs = self.cell_size
        try:
            with open(f'levelmaps/levelmap_{self.currentlevel}.csv', encoding="utf8") as csvfile1:
                reader1 = csv.reader(csvfile1, delimiter=';', quotechar='"')
                reader1 = list(reader1)
                with open(f'rooms/room_{reader1[self.current_room_y][self.current_room_x]}.csv', encoding="utf8") as csvfile:
                    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
                    reader = list(reader)
                    for y in range(self.height):
                        for x in range(self.width):
                            if reader[y][x] == '1':
                                screen.blit(self.border_image, (x * cs + self.left, y * cs + self.top))
                                self.room[y][x] = 1
                            if reader[y][x] == '2':
                                screen.blit(self.grass_image, (x * cs + self.left, y * cs + self.top))
                                self.room[y][x] = 2
                            if reader[y][x] == '4':
                                screen.blit(self.forest_exit_image, (x * cs + self.left, y * cs + self.top))
                                self.room[y][x] = 4

        except FileNotFoundError:
            sys.exit()

        #  boardcopy = pygame.Surface(screen.get_size())

        with open(f'objectmaps/objectmap_{self.pool_of_objectmaps[0]}.csv', encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            reader = list(reader)

            for y in range(self.height):
                for x in range(self.width):
                    if reader[y][x] == '3':
                        # boardcopy.blit(self.boulder_image, (x * cs + self.left, y * cs + self.top))
                        screen.blit(self.boulder_image, (x * cs + self.left, y * cs + self.top))
                        self.objects[y][x] = 3
                    # if reader[y][x] == '5':
                    #     # boardcopy.blit(self.mage_image, (x * cs + self.left, y * cs + self.top))
                    #     screen.blit(self.mage_image, (x * cs + self.left, y * cs + self.top))
                    #     self.objects[y][x] = 5

        for y in range(self.height):
            for x in range(self.width):
                if self.player[y][x] == '5':
                    screen.blit(self.mage_image, (x * cs + self.left, y * cs + self.top))

        #  screen.blit(boardcopy, (0, 0))

                # if (0 <= x <= 1 or 0 <= y <= 1 or self.width - 2 <= x <= self.width - 1 or
                #         self.height - 2 <= y <= self.height - 1):
                #     pygame.draw.rect(screen, pygame.Color('white'), (x * cs + self.left, y * cs + self.top, cs, cs))
                #     screen.blit(self.border_image, (x * cs + self.left, y * cs + self.top))
                #     self.mas[y][x] = 1
                # else:
                #     pygame.draw.rect(screen, pygame.Color('white'), (x * cs + self.left, y * cs + self.top, cs, cs))
                #     screen.blit(self.grass_image, (x * cs + self.left, y * cs + self.top))

        # screen.blit(self.mage_image, (self.where_x, self.where_y))

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
                state = self.room[coords[1]][coords[0]]
                if self.is_in_table(mp):
                    if state == 0:
                        self.room[coords[1]][coords[0]] = 1
                    else:
                        self.room[coords[1]][coords[0]] = 0
            coords[0] = xinst
            for y in range(self.height):
                coords[1] = y
                state = self.room[coords[1]][coords[0]]
                if self.is_in_table(mp):
                    if state == 0:
                        self.room[coords[1]][coords[0]] = 1
                    elif state == 1 and not y == yinst:
                        self.room[coords[1]][coords[0]] = 0


def main():
    pygame.init()
    running = True
    # xr = xl = yu = yd = False
    #  test_hero = load_image("mage_texture.png")

    width = 27
    height = 13
    left = 46
    top = 74
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

            if event.type == pygame.MOUSEBUTTONDOWN:
                board.map_number += 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    # yu = True
                    y, x = board.return_player_coords()
                    try:
                        if board.objects[y - 1][x] != 3 and board.room[y - 1][x] != 1:
                            if y - 1 >= 0:
                                board.player[y][x] = '0'
                                board.player[y - 1][x] = '5'
                            else:
                                board.current_room_y -= 1
                                board.player[y][x] = '0'
                                board.player[height - 1][x] = '5'
                        else:
                            board.current_room_y -= 1
                            board.player[y][x] = '0'
                            board.player[height - 1][x] = '5'
                    except IndexError:
                        pass

                if event.key == pygame.K_DOWN:
                    # yd = True
                    y, x = board.return_player_coords()
                    try:
                        if board.objects[y + 1][x] != 3 and board.room[y + 1][x] != 1:
                            board.player[y][x] = '0'
                            board.player[y + 1][x] = '5'
                    except IndexError:
                        board.player[y][x] = '0'
                        board.player[0][x] = '5'
                        board.current_room_y += 1

                if event.key == pygame.K_RIGHT:
                    # xr = True
                    y, x = board.return_player_coords()
                    try:
                        if board.objects[y][x + 1] != 3 and board.room[y][x + 1] != 1:
                            board.player[y][x] = '0'
                            board.player[y][x + 1] = '5'
                    except IndexError:
                        board.player[y][x] = '0'
                        board.player[y][0] = '5'
                        board.current_room_x += 1

                if event.key == pygame.K_LEFT:
                    # xl = True
                    y, x = board.return_player_coords()
                    try:
                        if board.objects[y][x - 1] != 3 and board.room[y][x - 1] != 1:
                            if x - 1 >= 0:
                                board.player[y][x] = '0'
                                board.player[y][x - 1] = '5'
                            else:
                                board.current_room_x -= 1
                                board.player[y][x] = '0'
                                board.player[y][width - 1] = '5'
                        else:
                            board.current_room_x -= 1
                            board.player[y][x] = '0'
                            board.player[y][width - 1] = '5'

                    except IndexError:
                        pass

            # if event.type == pygame.KEYUP:
            #     if event.key == pygame.K_UP:
            #         yu = False
            #     if event.key == pygame.K_DOWN:
            #         yd = False
            #     if event.key == pygame.K_RIGHT:
            #         xr = False
            #     if event.key == pygame.K_LEFT:
            #         xl = False

        # if xr:
        #     coords = board.where_x + 64, board.where_y
        #     if board.is_in_table(coords):
        #         board.where_x += 64
        #     xr = False
        # elif xl:
        #     coords = board.where_x - 64, board.where_y
        #     if board.is_in_table(coords):
        #         board.where_x -= 64
        #     xl = False
        # elif yu:
        #     coords = board.where_x, board.where_y - 64
        #     if board.is_in_table(coords):
        #         board.where_y -= 64
        #     yu = False
        # elif yd:
        #     coords = board.where_x, board.where_y + 64
        #     if board.is_in_table(coords):
        #         board.where_y += 64
        #     yd = False

        screen.fill((0, 0, 0))
        board.render(screen)

        pygame.display.flip()


if __name__ == '__main__':
    main()
