import pygame
import sys
import csv
from random import choice, randint
from pathlib import Path
from load_image_file import load_image
from animated_sprite import AnimatedSprite
from database_file import load_items_from_db, load_enemies_from_db, load_allies_from_db


# def write_csv(arr_save, name_csv):
#     csv.register_dialect('myDialect',
#     delimiter = '|',
#     quoting=csv.QUOTE_NONE,
#     skipinitialspace=True)
#     with open('debug\\' + name_csv + '.csv', 'w') as f:
#         writer = csv.writer(f, dialect='myDialect')
#         for row in arr_save:
#            writer.writerow(row)
#     f.close()


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


def x_and_y_from_game_map(game_map, room, x_cells, y_cells):
    for x in range(x_cells):
        for y in range(y_cells):
            if game_map[y][x] == str(room):
                return [x, y]


def return_from_id(id_inp, items):
    for i in range(len(items)):
        if items[i][0] == int(id_inp):
            return items[i]


class Board:
    #  Инициализируем класс Board. В него мы передаём количество клеток по x и y, размер клетки,
    #  отступы и информацию о персонажах
    def __init__(self, x_cells, y_cells, cell_size, top_indent, left_indent, player_data, character):
        #  Передаём объекту в собственность переданные переменные
        self.items_for_render = None
        self.player_data = player_data
        self.cs = cell_size
        self.room_for_render = []
        self.objectmap_for_render = []
        self.number_of_objects = []
        # self.items_map_for_current_level = [[['0'] * x_cells for _ in range(y_cells)] for _ in range(27)]
        self.objectmaps_for_current_level = [[0] * x_cells for _ in range(y_cells)]
        self.items_map_for_current_level = [[0] * x_cells for _ in range(y_cells)]
        self.screen_top = top_indent
        self.screen_left = left_indent

        self.character_inventory = {'70': [],
                                    '71': [],
                                    '72': [],
                                    '73': [],
                                    '74': [],
                                    '75': [],
                                    '76': [],
                                    }

        self.enemies_from_db = load_enemies_from_db()
        self.enemies = {'40': [],
                        '41': [],
                        '42': [],
                        '43': [],
                        '44': [],
                        }

        self.allies_from_db = load_allies_from_db(character)
        self.allies = {'31': [],
                       '32': [],
                       '33': [],
                       '34': []
                       }

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
            with open(f'map_folder\\maps\\map_{current_map}.csv', encoding="utf8") as csvfile:
                self.game_map = list(csv.reader(csvfile, delimiter=';', quotechar='"'))
                with open(f'map_folder\\levelmaps\\levelmap_{self.currentlevel}.csv', encoding="utf8") as csvfile_1:
                    levelmap = list(csv.reader(csvfile_1, delimiter=';', quotechar='"'))
                    self.levelmap_for_render = levelmap
                    for y in range(y_cells):
                        for x in range(x_cells):
                            current_room_number = int(self.game_map[y][x])
                            self.rooms_list[y][x] = current_room_number
                            if current_room_number != 0:
                                with open(f'map_folder\\rooms\\room_{levelmap[y][x]}.csv',
                                          encoding="utf8") as csvfile_2:
                                    room = list(csv.reader(csvfile_2, delimiter=';', quotechar='"'))
                                    self.rooms[current_room_number - 1] = room

            #  Создаём пул карт объектов
            objectmapsfolder = Path('map_folder\\objectmaps')
            number_of_objectmaps = len(list(objectmapsfolder.iterdir()))
            self.pool_of_objectmaps = [0] * number_of_objectmaps

            for x in range(1, number_of_objectmaps + 1):
                with open(f'map_folder\\objectmaps\\objectmap_{x}.csv', encoding="utf8") as csvfile_3:
                    objectmap = list(csv.reader(csvfile_3, delimiter=';', quotechar='"'))
                    self.pool_of_objectmaps[x - 1] = objectmap

            for y in range(y_cells):
                for x in range(x_cells):
                    self.objectmaps_for_current_level[y][x] = choice(self.pool_of_objectmaps)
                    self.items_map_for_current_level[y][x] = [['0'] * x_cells for _ in range(y_cells)]
                    # Случайно выбираем карты препятствий для уровня

            with open(f'map_folder\\objectnumber\\objectnumbermap_{self.currentlevel}.csv',
                      encoding="utf8") as csvfile_4:
                objectnumbermap = list(csv.reader(csvfile_4, delimiter=';', quotechar='"'))
                self.number_of_objects = objectnumbermap

            self.items = load_items_from_db()

            count_allies = 0
            for i in range(len(self.number_of_objects)):
                item_id = int(self.number_of_objects[i][0])
                item_number = int(self.number_of_objects[i][1])
                #  item_number = 100
                for j in range(item_number):
                    room_rnd = randint(2, value_of_rooms(self.currentlevel) - 1)
                    flag = True
                    x_and_y_from_game_map_current = x_and_y_from_game_map(self.game_map, room_rnd, x_cells, y_cells)
                    x, y = (x_and_y_from_game_map_current[0],
                            x_and_y_from_game_map_current[1])
                    while flag:
                        room_rnd_x = randint(2, x_cells - 3)
                        room_rnd_y = randint(3, y_cells - 3)
                        if self.objectmaps_for_current_level[y][x][room_rnd_y][room_rnd_x] == '2':
                            if self.items_map_for_current_level[y][x][room_rnd_y][room_rnd_x] == '0':
                                if str(item_id) in [f'{h}' for h in range(50, 77)]:
                                    self.items_map_for_current_level[y][x][room_rnd_y][room_rnd_x] = str(item_id)

                                if str(item_id) in [f'{h}' for h in range(40, 45)]:
                                    self.enemies[str(item_id)].append([randint(self.enemies_from_db[str(item_id)][3],
                                                                               self.enemies_from_db[str(item_id)][4]),
                                                                       randint(self.enemies_from_db[str(item_id)][5],
                                                                               self.enemies_from_db[str(item_id)][6]),
                                                                       randint(self.enemies_from_db[str(item_id)][7],
                                                                               self.enemies_from_db[str(item_id)][8]),
                                                                       y, x, room_rnd_y, room_rnd_x])
                                    self.items_map_for_current_level[y][x][room_rnd_y][room_rnd_x] = str(item_id)

                                    if count_allies < 3:
                                        for id_allies in range(31, 35):
                                            if id_allies == self.player_data[5] or len(
                                                self.allies[str(id_allies)]) != 0: continue
                                            add_allies = False
                                            flag2 = True
                                            while flag2:
                                                room_rnd2_x = randint(2, x_cells - 3)
                                                room_rnd2_y = randint(3, y_cells - 3)
                                                if self.objectmaps_for_current_level[y][x][room_rnd2_y][
                                                    room_rnd2_x] == '2':
                                                    if self.items_map_for_current_level[y][x][room_rnd2_y][
                                                        room_rnd2_x] == '0':
                                                        self.allies[str(id_allies)].append(
                                                            [randint(self.allies_from_db[str(id_allies)][3],
                                                                     self.allies_from_db[str(id_allies)][4]),
                                                             randint(self.allies_from_db[str(id_allies)][5],
                                                                     self.allies_from_db[str(id_allies)][6]),
                                                             randint(self.allies_from_db[str(id_allies)][7],
                                                                     self.allies_from_db[str(id_allies)][8]),
                                                             # 6, 13, room_rnd_y, room_rnd_x])
                                                             y, x, room_rnd2_y, room_rnd2_x])
                                                        self.items_map_for_current_level[y][x][room_rnd2_y][
                                                            room_rnd2_x] = str(id_allies)
                                                        count_allies += 1
                                                        add_allies = True
                                                        flag2 = False
                                            if add_allies: break
                                # if str(item_id) in [f'{n}' for n in range(31, 35)]:
                                #     find_enemies_in_room = False
                                #     for yy in range(y_cells):
                                #         for xx in range(x_cells):
                                #             if items_map_for_current_level[y][x][room_rnd_y][room_rnd_x]
                                #     if self.allies_from_db[str(item_id)] is not None:
                                #         self.allies[str(item_id)].append([randint(self.allies_from_db[str(item_id)][3],
                                #                                                   self.allies_from_db[str(item_id)][4]),
                                #                                           randint(self.allies_from_db[str(item_id)][5],
                                #                                                   self.allies_from_db[str(item_id)][6]),
                                #                                           randint(self.allies_from_db[str(item_id)][7],
                                #                                                   self.allies_from_db[str(item_id)][8]),
                                #                                           6, 13, room_rnd_y, room_rnd_x])
                                #                                           #y, x, room_rnd_y, room_rnd_x])

                                flag = False

        #  Выходим, если искомого файла не существует
        except FileNotFoundError:
            # print(current_map)
            # print(self.currentlevel)
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
        #  self.mage_image = load_image("mage_texture.png")

        self.mage_sprite = AnimatedSprite(load_image("mage_texture2.png"), 4, 4, 64, 64)
        self.mage_image = self.mage_sprite.frames[self.mage_sprite.cur_frame]
        self.forester_sprite = AnimatedSprite(load_image("forester_texture2.png"), 4, 4, 64, 64)
        self.forester_image = self.forester_sprite.frames[self.forester_sprite.cur_frame]
        self.fool_sprite = AnimatedSprite(load_image("fool_texture2.png"), 4, 4, 64, 64)
        self.fool_image = self.fool_sprite.frames[self.fool_sprite.cur_frame]
        self.anarchist_sprite = AnimatedSprite(load_image("anarchist_texture2.png"), 4, 4, 64, 64)
        self.anarchist_image = self.anarchist_sprite.frames[self.anarchist_sprite.cur_frame]

        self.skeleton_sprite = AnimatedSprite(load_image("skeleton.png"), 8, 1, 64, 64)
        self.skeleton_image = self.skeleton_sprite.frames[self.skeleton_sprite.cur_frame]
        self.daemon_sprite = AnimatedSprite(load_image("daemon.png"), 8, 1, 64, 64)
        self.daemon_image = self.daemon_sprite.frames[self.daemon_sprite.cur_frame]
        self.frogger_sprite = AnimatedSprite(load_image("frogger.png"), 4, 1, 128, 128)
        self.frogger_image = self.frogger_sprite.frames[self.frogger_sprite.cur_frame]

        if character == 'Маг':
            self.player_sprite = self.mage_sprite
            self.player_image = self.mage_image
        if character == 'Лесник':
            self.player_sprite = self.forester_sprite
            self.player_image = self.forester_image
        if character == 'Шут':
            self.player_sprite = self.fool_sprite
            self.player_image = self.fool_image
        if character == 'Анархист':
            self.player_sprite = self.anarchist_sprite
            self.player_image = self.anarchist_image

        self.boulder_image = load_image("boulder_image.png")

        self.forest_exit_up_image = load_image("forest_exit_up.png")
        self.forest_exit_down_image = load_image("forest_exit_down.png")
        self.forest_exit_right_image = load_image("forest_exit_right.png")
        self.forest_exit_left_image = load_image("forest_exit_left.png")

        self.items_images = {'50': load_image("red_cr.png"),
                             '51': load_image("blue_cr.png"),
                             '52': load_image("green_cr.png"),
                             '53': load_image("purple_cr.png"),
                             '70': load_image("helmet.png"),
                             '71': load_image("sword.png"),
                             '72': load_image("bow.png"),
                             '73': load_image("armor.png"),
                             '74': load_image("knife.png"),
                             '75': load_image("shield.png"),
                             '76': load_image("magic_staff.png"),
                             }

    #  Функция отрисовки всей игры. Используя инициализированные списки комнат/объектов и пр.,
    #  отрисовывает игровую ситуацию.
    def game_render(self, screen):
        self.room_for_render = self.rooms[int(self.game_map[self.current_room_y][self.current_room_x]) - 1]
        self.objectmap_for_render = self.objectmaps_for_current_level[self.current_room_y][self.current_room_x]
        self.items_for_render = self.items_map_for_current_level[self.current_room_y][self.current_room_x]
        self.seen[self.current_room_y][self.current_room_x] = 1
        #  В зависимости от символов в картах уровня читаем их и отрисовываем на игровом экране
        for y in range(self.height_in_cells):
            for x in range(self.width_in_cells):
                if self.room_for_render[y][x] == '1':
                    screen.blit(self.border_image, (x * self.cs + self.left, y * self.cs + self.top))
                if self.room_for_render[y][x] == '2':
                    screen.blit(self.grass_image, (x * self.cs + self.left, y * self.cs + self.top))

                if self.room_for_render[y][x] == '4' and y == 0:
                    screen.blit(self.forest_exit_up_image, (x * self.cs + self.left, y * self.cs + self.top))
                if self.room_for_render[y][x] == '4' and y == self.height_in_cells - 1:
                    screen.blit(self.forest_exit_down_image, (x * self.cs + self.left, y * self.cs + self.top))
                if self.room_for_render[y][x] == '4' and x == 0:
                    screen.blit(self.forest_exit_left_image, (x * self.cs + self.left, y * self.cs + self.top))
                if self.room_for_render[y][x] == '4' and x == self.width_in_cells - 1:
                    screen.blit(self.forest_exit_right_image, (x * self.cs + self.left, y * self.cs + self.top))

                if self.objectmap_for_render[y][x] == '3':
                    screen.blit(self.boulder_image, (x * self.cs + self.left, y * self.cs + self.top))
                # if self.objectmap_for_render[y][x] == '3':
                #     self.skeleton_image = self.skeleton_sprite.frames[self.skeleton_sprite.cur_frame]
                #     screen.blit(self.skeleton_image, (x * self.cs + self.left, y * self.cs + self.top))
                if self.items_for_render[y][x] == '40':
                    self.daemon_image = self.daemon_sprite.frames[self.daemon_sprite.cur_frame]
                    screen.blit(self.daemon_image, (x * self.cs + self.left, y * self.cs + self.top))
                if self.items_for_render[y][x] == '43':
                    self.skeleton_image = self.skeleton_sprite.frames[self.skeleton_sprite.cur_frame]
                    screen.blit(self.skeleton_image, (x * self.cs + self.left, y * self.cs + self.top))
                if self.items_for_render[y][x] in [f'{j}' for j in range(50, 77)]:
                    # screen.blit(load_image(f'{return_from_id(self.items_for_render[y][x], self.items)[2]}.png'),
                    #             (x * self.cs + self.left, y * self.cs + self.top))
                    # screen.blit(load_image(f'{return_from_id(self.items_for_render[y][x], self.items)[2]}.png'),
                    #             (x * self.cs + self.left, y * self.cs + self.top))
                    screen.blit(self.items_images[self.items_for_render[y][x]],
                                (x * self.cs + self.left, y * self.cs + self.top))
                if self.items_for_render[y][x] in [f'{j}' for j in range(31, 35)]:
                    if self.allies[self.items_for_render[y][x]]:
                        if self.items_for_render[y][x] == '31':
                            screen.blit(self.mage_image, (x * self.cs + self.left, y * self.cs + self.top))
                        if self.items_for_render[y][x] == '32':
                            screen.blit(self.forester_image, (x * self.cs + self.left, y * self.cs + self.top))
                        if self.items_for_render[y][x] == '33':
                            screen.blit(self.fool_image, (x * self.cs + self.left, y * self.cs + self.top))
                        if self.items_for_render[y][x] == '34':
                            screen.blit(self.anarchist_image, (x * self.cs + self.left, y * self.cs + self.top))
                if self.player[y][x] == '5':
                    self.player_image = self.player_sprite.frames[self.player_sprite.cur_frame]
                    screen.blit(self.player_image, (x * self.cs + self.left, y * self.cs + self.top))

        #  Блок установки шрифта для дальнейшего вывода надписей:
        text_font = pygame.font.Font('fonts\\Hombre Regular.otf', 40)
        hp_text = text_font.render(f'Здоровье:{self.player_data[0]}', 1, (180, 0, 0))
        screen.blit(hp_text, (self.screen_left, self.screen_top // 4))

        damage_text = text_font.render(f'Урон:{self.player_data[1]}', 1, (128, 128, 128))
        screen.blit(damage_text, (self.screen_left * 6 - 5, self.screen_top // 4))

        protection_text = text_font.render(f'Защита:{self.player_data[2]}', 1, (244, 169, 0))
        screen.blit(protection_text, (self.screen_left * 9 + 20, self.screen_top // 4))

        energy_text = text_font.render(f'Энергия:{self.player_data[3]}', 1, (0, 77, 255))
        screen.blit(energy_text, (self.screen_left * 13 + 15, self.screen_top // 4))

        luck_text = text_font.render(f'Удача:{self.player_data[4]}', 1, (0, 128, 0))
        screen.blit(luck_text, (self.screen_left * 17 + 30, self.screen_top // 4))

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

    def inventory_render(self, screen):
        #  Отрисовка карты игры. Сначала заливает весь экран бледно-зелёным
        screen.fill((0, 0, 0))

        intro_text = ["ИНВЕНТАРЬ:",
                      "",
                      f"ШЛЕМ                КОЛ-ВО: {len(self.character_inventory['70'])}",
                      f"МЕЧ                 КОЛ-ВО: {len(self.character_inventory['71'])}",
                      f"ЛУК                 КОЛ-ВО: {len(self.character_inventory['72'])}",
                      f"ДОСПЕХИ             КОЛ-ВО: {len(self.character_inventory['73'])}",
                      f"НОЖ                 КОЛ-ВО: {len(self.character_inventory['74'])}",
                      f"ЩИТ                 КОЛ-ВО: {len(self.character_inventory['75'])}",
                      f"ВОЛШЕБНЫЙ ПОСОХ     КОЛ-ВО: {len(self.character_inventory['76'])}",
                      "",
                      "Чтобы выйти из инвентаря нажмите I"]

        font = pygame.font.Font('fonts\\Hombre Regular.otf', 60)
        text_coord = 25
        first_letter = True
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('WHITE'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            if first_letter:
                intro_rect.x = 750
                first_letter = False
            else:
                intro_rect.x = 550
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

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
