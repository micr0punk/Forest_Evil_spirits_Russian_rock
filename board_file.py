import pygame
import sys
import csv
from random import choice
from pathlib import Path
from load_image_file import load_image
from animated_sprite import AnimatedSprite


#  Создаём функцию, которая вычисляет количество номерных карт уровней
def value_of_rooms(current_map):
    current_number_of_rooms = 0
    with open(f'map_folder\\maps/map_{current_map}.csv', encoding="utf8") as csvfile:
        reader = list(csv.reader(csvfile, delimiter=';', quotechar='"'))
        for x in range(len(reader)):
            for y in range(len(reader[x])):
                if reader[x][y] != '0':
                    current_number_of_rooms += 1

    #  Возвращаем кол-во комнат
    return current_number_of_rooms


class Board:
    #  Инициализируем класс Board. В него мы передаём количество клеток по x и y, размер клетки,
    #  отступы и информацию о персонажах
    def __init__(self, x_cells, y_cells, cell_size, top_indent, left_indent, player_data):
        #  Передаём объекту в собственность переданные переменные
        self.player_data = player_data
        self.cs = cell_size
        self.room_for_render = []
        self.objectmap_for_render = []
        self.screen_top = top_indent
        self.screen_left = left_indent

        #  Задаём пул номерных карт и текущую карту
        maps_folder = Path('map_folder\\maps')
        number_of_maps = len(list(maps_folder.iterdir()))
        pool_of_maps = [number for number in range(1, number_of_maps + 1)]
        current_map = choice(pool_of_maps)

        #  Задаём пул карт уровней и текущую карту уровня
        levelmaps_folder = Path('map_folder\\levelmaps')
        number_of_levelmaps = len(list(levelmaps_folder.iterdir()))
        pool_of_levelmaps = [number for number in range(1, number_of_levelmaps + 1)]
        self.currentlevel = choice(pool_of_levelmaps)

        self.currentlevel = current_map

        self.rooms_list = [[0] * x_cells for _ in range(y_cells)]

        #  self.

        try:
            #  Инициализируем трёхмерный список всех комнат уровня единожды, при создании объекта
            self.rooms = [0] * value_of_rooms(current_map)
            with open(f'map_folder\\maps/map_{current_map}.csv', encoding="utf8") as csvfile:
                self.game_map = list(csv.reader(csvfile, delimiter=';', quotechar='"'))
                with open(f'map_folder\\levelmaps/levelmap_{self.currentlevel}.csv', encoding="utf8") as csvfile_1:
                    levelmap = list(csv.reader(csvfile_1, delimiter=';', quotechar='"'))
                    self.levelmap_for_render = levelmap
                    for y in range(y_cells):
                        for x in range(x_cells):
                            current_room_number = int(self.game_map[y][x])
                            self.rooms_list[y][x] = current_room_number
                            if current_room_number != 0:
                                with open(f'map_folder\\rooms/room_{levelmap[y][x]}.csv', encoding="utf8") as csvfile_2:
                                    room = list(csv.reader(csvfile_2, delimiter=';', quotechar='"'))
                                    self.rooms[current_room_number - 1] = room

            #  Создаём пул карт объектов
            objectmapsfolder = Path('map_folder\\objectmaps')
            number_of_objectmaps = len(list(objectmapsfolder.iterdir()))
            self.pool_of_objectmaps = [0] * number_of_objectmaps

            for x in range(1, number_of_objectmaps + 1):
                with open(f'map_folder\\objectmaps/objectmap_{x}.csv', encoding="utf8") as csvfile_3:
                    objectmap = list(csv.reader(csvfile_3, delimiter=';', quotechar='"'))
                    self.pool_of_objectmaps[x - 1] = objectmap

            self.objectmaps_for_current_level = [[0] * x_cells for _ in range(y_cells)]

            for y in range(y_cells):
                for x in range(x_cells):
                    self.objectmaps_for_current_level[y][x] = choice(self.pool_of_objectmaps)
                    # Случайно выбираем карты препятствий для уровня

        #  Выходим, если искомого файла не существует
        except FileNotFoundError:
            print(current_map)
            print(self.currentlevel)
            print('Не удалось загрузить файл/ы')
            sys.exit()

        # print(self.rooms)
        # print(self.rooms_list)

        #  Текущая комната – это всегда центр всех csv файлов игры, 13 и 6
        self.current_room_x, self.current_room_y = 13, 6

        #  Создаю дополнительные массивы и инициализирую дополнительные переменные
        self.width_in_cells = x_cells
        self.height_in_cells = y_cells

        self.seen = [[0] * x_cells for _ in range(y_cells)]
        self.player = [[0] * x_cells for _ in range(y_cells)]
        self.player[y_cells // 2][x_cells // 2] = '5'

        self.left = 10
        self.top = 10

        # Передача в класс Board текстур разных поверхностей и персонажей
        self.grass_image = load_image("grass_image.png")
        self.border_image = load_image("border_image.png")
        #  self.mage_image = load_image("mage_texture2.png")
        self.mage_sprite = AnimatedSprite(load_image("mage_texture2.png"), 4, 4, 64, 64)
        self.mage_image = self.mage_sprite.frames[self.mage_sprite.cur_frame]
        self.boulder_image = load_image("boulder_image.png")
        self.forest_exit_image = load_image("forest_exit.png")
        self.prize_plate = load_image("item_slot.png")

    #  Функция отрисовки всей игры. Используя инициализированные списки комнат/объектов и пр.,
    #  отрисовывает игровую ситуацию.
    def game_render(self, screen, width, height):
        self.room_for_render = self.rooms[int(self.game_map[self.current_room_y][self.current_room_x]) - 1]
        self.objectmap_for_render = self.objectmaps_for_current_level[self.current_room_y][self.current_room_x]
        self.seen[self.current_room_y][self.current_room_x] = 1
        #  В зависимости от символов в картах уровня читаем их и отрисовываем на игровом экране
        for y in range(self.height_in_cells):
            for x in range(self.width_in_cells):
                if self.room_for_render[y][x] == '1':
                    screen.blit(self.border_image, (x * self.cs + self.left, y * self.cs + self.top))
                if self.room_for_render[y][x] == '2':
                    screen.blit(self.grass_image, (x * self.cs + self.left, y * self.cs + self.top))
                if self.room_for_render[y][x] == '4':
                    screen.blit(self.forest_exit_image, (x * self.cs + self.left, y * self.cs + self.top))
                if self.objectmap_for_render[y][x] == '3':
                    screen.blit(self.boulder_image, (x * self.cs + self.left, y * self.cs + self.top))
                if self.player[y][x] == '5':
                    self.mage_image = self.mage_sprite.frames[self.mage_sprite.cur_frame]
                    screen.blit(self.mage_image, (x * self.cs + self.left, y * self.cs + self.top))


        #  Блок установки шрифта для дальнейшего вывода надписей:
        text_font = pygame.font.Font('fonts\\Hombre Regular.otf', 40)
        hp_text = text_font.render(f'Здоровье:{self.player_data[5]}', 1, (180, 0, 0))
        screen.blit(hp_text, (self.screen_left, self.screen_top // 4))

        damage_text = text_font.render(f'Урон:{self.player_data[6]}', 1, (128, 128, 128))
        screen.blit(damage_text, (self.screen_left * 6, self.screen_top // 4))

        energy_text = text_font.render(f'Энергия:{self.player_data[7]}', 1, (0, 77, 255))
        screen.blit(energy_text, (self.screen_left * 10, self.screen_top // 4))

    # Возвращает координаты персонажа в Y и в X
    def return_player_coords(self):
        for y in range(self.height_in_cells):
            for x in range(self.width_in_cells):
                if self.player[y][x] == '5':
                    return y, x

    #  Функция, позволяющая управлять параметрами игрового окна.
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cs = cell_size

    def map_render(self, screen, is_minimap=None):
        #  Отрисовка карты игры. Сначала заливает весь экран бледно-зелёным
        screen.fill((68, 148, 74))
        for y in range(self.height_in_cells):
            for x in range(self.width_in_cells):
                if self.seen[y][x] == 1:
                    #  отрисовка карты
                    pygame.draw.rect(screen, pygame.Color('white'),
                                     (x * self.cs + self.left, y * self.cs + self.top, self.cs, self.cs))
                    pygame.draw.rect(screen, pygame.Color('brown'),
                                     (x * self.cs + self.left, y * self.cs + self.top, self.cs, self.cs), 1)

                    reader1 = self.levelmap_for_render
                    #  Так как при обычном рендере мы записали в self.seen позиции где бы и не был персонаж,
                    #  то мы можем с огромной лёгкостью отрисовать карту
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

    # Работает в паре с get_cell
    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)

    # После нажатия кнопкой мыши возвращает клетку, в которой произошло нажатие
    def get_cell(self, mp):
        where_x, where_y = mp
        if self.left <= where_x <= self.left + self.cs * self.width_in_cells and \
                self.top <= where_y <= self.top + self.cs * self.height_in_cells:
            return where_x // self.cs - 2, where_y // self.cs - 2
        else:
            return None

    #  Функция. Возвращает True, если координаты нажатия кнопкой мыши находятся в пределах игрового поля
    def is_in_table(self, mp):
        where_x, where_y = mp
        if self.left <= where_x <= self.left + self.cs * self.width_in_cells and \
                self.top <= where_y <= self.top + self.cs * self.height_in_cells:
            return True
        else:
            return False
