import pygame
import sys
import csv
from random import choice
from pathlib import Path
import load_image_file


def value_of_rooms(current_map):
    current_number_of_rooms = 0
    with open(f'maps/map_{current_map}.csv', encoding="utf8") as csvfile:
        reader = list(csv.reader(csvfile, delimiter=';', quotechar='"'))
        for x in range(len(reader)):
            for y in range(len(reader[x])):
                if reader[x][y] != '0':
                    current_number_of_rooms += 1

    return current_number_of_rooms


class Board:
    def __init__(self, width, height, cell_size, top, left, player_data):
        self.player_data = player_data
        self.cs = cell_size
        self.room_for_render = []
        self.objectmap_for_render = []
        self.screen_top = top
        self.screen_left = left

        maps_folder = Path('maps')
        number_of_maps = len(list(maps_folder.iterdir()))
        pool_of_maps = [number for number in range(1, number_of_maps + 1)]
        current_map = choice(pool_of_maps)

        levelmaps_folder = Path('levelmaps')
        number_of_levelmaps = len(list(levelmaps_folder.iterdir()))
        pool_of_levelmaps = [number for number in range(1, number_of_levelmaps + 1)]
        self.currentlevel = choice(pool_of_levelmaps)

        self.rooms_list = [[0] * width for _ in range(height)]

        try:
            self.rooms = [0] * value_of_rooms(current_map)
            with open(f'maps/map_{current_map}.csv', encoding="utf8") as csvfile:
                self.game_map = list(csv.reader(csvfile, delimiter=';', quotechar='"'))
                with open(f'levelmaps/levelmap_{self.currentlevel}.csv', encoding="utf8") as csvfile_1:
                    levelmap = list(csv.reader(csvfile_1, delimiter=';', quotechar='"'))
                    for y in range(height):
                        for x in range(width):
                            current_room_number = int(self.game_map[y][x])
                            self.rooms_list[y][x] = current_room_number
                            if current_room_number != 0:
                                with open(f'rooms/room_{levelmap[y][x]}.csv', encoding="utf8") as csvfile_2:
                                    room = list(csv.reader(csvfile_2, delimiter=';', quotechar='"'))
                                    self.rooms[current_room_number - 1] = room

            objectmapsfolder = Path('objectmaps')
            number_of_objectmaps = len(list(objectmapsfolder.iterdir()))
            self.pool_of_objectmaps = [0] * number_of_objectmaps

            for x in range(1, number_of_objectmaps + 1):
                with open(f'objectmaps/objectmap_{x}.csv', encoding="utf8") as csvfile_3:
                    objectmap = list(csv.reader(csvfile_3, delimiter=';', quotechar='"'))
                    self.pool_of_objectmaps[x - 1] = objectmap

            self.objectmaps_for_current_level = [[0] * width for _ in range(height)]

            for y in range(height):
                for x in range(width):
                    self.objectmaps_for_current_level[y][x] = choice(self.pool_of_objectmaps)

        except FileNotFoundError:
            sys.exit()

        # print(self.rooms)
        # print(self.rooms_list)

        self.current_room_x, self.current_room_y = 13, 6

        self.width = width
        self.height = height

        self.seen = [[0] * width for _ in range(height)]
        self.player = [[0] * width for _ in range(height)]
        self.player[height // 2][width // 2] = '5'

        self.left = 10
        self.top = 10

        # Загрузка в класс Board текстур разных поверхностей и персонажей
        self.grass_image = load_image_file.load_image("grass_image.png")
        self.border_image = load_image_file.load_image("border_image.png")
        self.mage_image = load_image_file.load_image("mage_texture2.png")
        self.boulder_image = load_image_file.load_image("boulder_image.png")
        self.forest_exit_image = load_image_file.load_image("forest_exit.png")
        self.prize_plate = load_image_file.load_image("item_slot.png")

    def new_render(self, screen, width, height):
        self.room_for_render = self.rooms[int(self.game_map[self.current_room_y][self.current_room_x]) - 1]
        self.objectmap_for_render = self.objectmaps_for_current_level[self.current_room_y][self.current_room_x]
        self.seen[self.current_room_y][self.current_room_x] = 1
        for y in range(self.height):
            for x in range(self.width):
                if self.room_for_render[y][x] == '1':
                    screen.blit(self.border_image, (x * self.cs + self.left, y * self.cs + self.top))
                if self.room_for_render[y][x] == '2':
                    screen.blit(self.grass_image, (x * self.cs + self.left, y * self.cs + self.top))
                if self.room_for_render[y][x] == '4':
                    screen.blit(self.forest_exit_image, (x * self.cs + self.left, y * self.cs + self.top))
                if self.objectmap_for_render[y][x] == '3':
                    screen.blit(self.boulder_image, (x * self.cs + self.left, y * self.cs + self.top))
                if self.player[y][x] == '5':
                    screen.blit(self.mage_image, (x * self.cs + self.left, y * self.cs + self.top))

        text_font = pygame.font.Font('fonts\\Hombre Regular.otf', 40)
        hp_text = text_font.render(f'Здоровье:{self.player_data[5]}', 1, (180, 0, 0))
        screen.blit(hp_text, (self.screen_left, self.screen_top // 4))

        damage_text = text_font.render(f'Урон:{self.player_data[6]}', 1, (128, 128, 128))
        screen.blit(damage_text, (self.screen_left * 6, self.screen_top // 4))

        energy_text = text_font.render(f'Энергия:{self.player_data[7]}', 1, (0, 77, 255))
        screen.blit(energy_text, (self.screen_left * 10, self.screen_top // 4))

    def return_player_coords(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.player[y][x] == '5':
                    return y, x

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def map_render(self, screen):
        screen.fill((68, 148, 74))
        for y in range(self.height):
            for x in range(self.width):
                if self.seen[y][x] == 1:
                    pygame.draw.rect(screen, pygame.Color('white'),
                                     (x * self.cs + self.left, y * self.cs + self.top, self.cs, self.cs))
                    pygame.draw.rect(screen, pygame.Color('brown'),
                                     (x * self.cs + self.left, y * self.cs + self.top, self.cs, self.cs), 1)
                    with open(f'levelmaps/levelmap_{self.currentlevel}.csv', encoding="utf8") as csvfile1:
                        reader1 = csv.reader(csvfile1, delimiter=';', quotechar='"')
                        reader1 = list(reader1)
                        if reader1[y][x + 1] != '0' and self.seen[y][x + 1] != 1:
                            pygame.draw.rect(screen, pygame.Color('black'),
                                             (x * self.cs + self.left + self.cs, y * self.cs + self.top,
                                              self.cs, self.cs))
                            pygame.draw.rect(screen, pygame.Color('brown'),
                                             (x * self.cs + self.left + self.cs, y * self.cs + self.top,
                                              self.cs, self.cs), 1)
                        if reader1[y][x - 1] != '0' and self.seen[y][x - 1] != 1:
                            pygame.draw.rect(screen, pygame.Color('black'),
                                             (x * self.cs + self.left - self.cs, y * self.cs + self.top,
                                              self.cs, self.cs))
                            pygame.draw.rect(screen, pygame.Color('brown'),
                                             (x * self.cs + self.left - self.cs, y * self.cs + self.top,
                                              self.cs, self.cs), 1)
                        if reader1[y + 1][x] != '0' and self.seen[y + 1][x] != 1:
                            pygame.draw.rect(screen, pygame.Color('black'),
                                             (x * self.cs + self.left, y * self.cs + self.top + self.cs,
                                              self.cs, self.cs))
                            pygame.draw.rect(screen, pygame.Color('brown'),
                                             (x * self.cs + self.left, y * self.cs + self.top + self.cs,
                                              self.cs, self.cs), 1)
                        if reader1[y - 1][x] != '0' and self.seen[y - 1][x] != 1:
                            pygame.draw.rect(screen, pygame.Color('black'),
                                             (x * self.cs + self.left, y * self.cs + self.top - self.cs,
                                              self.cs, self.cs))
                            pygame.draw.rect(screen, pygame.Color('brown'),
                                             (x * self.cs + self.left, y * self.cs + self.top - self.cs,
                                              self.cs, self.cs), 1)
                if self.current_room_x == x and self.current_room_y == y:
                    cs1 = self.cs // 2
                    pygame.draw.rect(screen, pygame.Color('black'),
                                     (x * self.cs + self.left + cs1 // 2, y * self.cs + self.top + cs1 // 2, cs1, cs1))

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
