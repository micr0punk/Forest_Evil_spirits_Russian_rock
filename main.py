import sys
from random import randint
import traceback

import pygame

import board_file
from characters import Mage, Forester, Fool, Anarchist
from database_file import load_character_from_db
from load_image_file import load_image

FPS = 60

#  Задаём разрешение игры в пикселях
size = width_in_pixels, height_in_pixels = 1820, 980

#  Задаём экран, с которым будем работать
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

victory = False


def victory_screen():
    pygame.init()

    screen.fill((0, 0, 0))
    font = pygame.font.Font('fonts\\Hombre Regular.otf', 120)
    string_rendered = font.render('ВЫ ПОБЕДИЛИ!', 1, pygame.Color('WHITE'))
    screen.blit(string_rendered, (1920 // 4 + 30, 1080 // 4 + 30))
    font = pygame.font.Font('fonts\\Hombre Regular.otf', 60)
    string_rendered = font.render('Для выхода, нажмите SPACE', 1, pygame.Color('WHITE'))
    screen.blit(string_rendered, (580, 720))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    sys.exit()
        pygame.display.flip()
        clock.tick(FPS)


def game_over():
    pygame.init()

    screen.fill((0, 0, 0))
    font = pygame.font.Font('fonts\\Hombre Regular.otf', 120)
    string_rendered = font.render('ИГРА ОКОНЧЕНА!', 1, pygame.Color('WHITE'))
    screen.blit(string_rendered, (1920 // 4 - 15, 1080 // 4 + 30))
    font = pygame.font.Font('fonts\\Hombre Regular.otf', 60)
    string_rendered = font.render('Для выхода, нажмите SPACE', 1, pygame.Color('WHITE'))
    screen.blit(string_rendered, (580, 720))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    sys.exit()
        pygame.display.flip()
        clock.tick(FPS)


def battle_screen(map_y, map_x, room_y, room_x, itemmap, character_name, character_mas, enemy_name, enemy_mas,
                  is_there_item=False, item_name=None, item=None,
                  is_there_allie=False, allie=None):
    # pygame.init()

    who_is_first_bool = randint(0, 1)
    who_is_first_bool_is_showed = False

    used_item = False
    battle_in_progress = False

    screen.fill((0, 0, 0))
    font = pygame.font.Font('fonts\\Hombre Regular.otf', 120)
    string_rendered = font.render('ВАС АТАКОВАЛИ!', 1, pygame.Color('WHITE'))
    screen.blit(string_rendered, (1920 // 4 + 15, 1080 // 4 + 30))
    font = pygame.font.Font('fonts\\Hombre Regular.otf', 60)
    string_rendered = font.render('Для продолжения, нажмите SPACE', 1, pygame.Color('WHITE'))
    screen.blit(string_rendered, (530, 720))

    def used_item_func():
        screen.fill((0, 0, 0))
        string_renderedd = font.render(f'ВЫ ИСПОЛЬЗОВАЛИ  {item_name.upper()}', 1, pygame.Color('WHITE'))
        screen.blit(string_renderedd, (1920 // 4 + 50, 1080 // 4 + 100))
        return

    def attacked_func(damage_pl):
        screen.fill((0, 0, 0))
        string_renderedd = font.render(f'ВЫ АТАКОВАЛИ  {enemy_name.upper()}А', 1, pygame.Color('WHITE'))
        screen.blit(string_renderedd, (1920 // 4 + 110, 1080 // 4 + 150))
        string_renderedd = font.render(f'НАНЕСЕНО {damage_pl} УРОНА', 1, pygame.Color('WHITE'))
        screen.blit(string_renderedd, (1920 // 4 + 175, 1080 // 4 + 230))
        return

    def being_attacked_func(damage_enemy):
        screen.fill((0, 0, 0))
        string_renderedd = font.render(f'{enemy_name.upper()} АТАКОВАЛ ВАС', 1, pygame.Color('WHITE'))
        screen.blit(string_renderedd, (1920 // 4 + 110, 1080 // 4 + 150))
        string_renderedd = font.render(f'НАНЕСЕНО {damage_enemy} УРОНА', 1, pygame.Color('WHITE'))
        screen.blit(string_renderedd, (1920 // 4 + 155, 1080 // 4 + 230))
        return

    def who_is_first(who):
        screen.fill((0, 0, 0))
        if who:
            string_renderedd = font.render(f'{character_name.upper()} НАЧИНАЕТ ПЕРВЫЙ', 1, pygame.Color('WHITE'))
            screen.blit(string_renderedd, (1920 // 4 + 50, 1080 // 4 + 100))
            return
        else:
            string_renderedd = font.render(f'{enemy_name.upper()} НАЧИНАЕТ ПЕРВЫЙ', 1, pygame.Color('WHITE'))
            screen.blit(string_renderedd, (1920 // 4 + 50, 1080 // 4 + 100))
            return

    def battle(font_from_init, allie_state, allie_name, item_state, item_name_str, item_mas):
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, pygame.Color('WHITE'),
                         (0, 628, 1820, 350), 1)
        pygame.draw.rect(screen, pygame.Color('WHITE'),
                         (0, 0, 1820 // 2, 628), 1)
        pygame.draw.rect(screen, pygame.Color('WHITE'),
                         (1820 // 2, 0, 1820 // 2, 628), 1)

        character_text = [f"{character_name.upper()}",
                          "",
                          f"ЗДОРОВЬЕ: {character_mas[0]}",
                          f"УРОН: {character_mas[1]}",
                          f"ЗАЩИТА: {character_mas[2]}",
                          f"ЭНЕРГИЯ: {character_mas[3]}",
                          f"УДАЧА: {character_mas[4]}"

                          ]

        enemy_text = [f"{enemy_name.upper()}",
                      "",
                      f"ЗДОРОВЬЕ: {enemy_mas[0]}",
                      f"УРОН: {enemy_mas[1]}",
                      f"ЗАЩИТА: {enemy_mas[2]}",

                      ]

        text_coord = 10
        for line in character_text:
            string_rendered_print = font_from_init.render(line, 1, pygame.Color('WHITE'))
            intro_rect = string_rendered_print.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 70
            text_coord += intro_rect.height
            screen.blit(string_rendered_print, intro_rect)

        text_coord = 5
        for line in enemy_text:
            string_rendered_print = font_from_init.render(line, 1, pygame.Color('WHITE'))
            intro_rect = string_rendered_print.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 970
            text_coord += intro_rect.height
            screen.blit(string_rendered_print, intro_rect)

        attack_string = font.render('A - атаковать', 1, pygame.Color('WHITE'))
        screen.blit(attack_string, (70, 780))
        if item_state:
            using_string = font.render(f'Текущий предмет: {item_name_str}', 1, pygame.Color('WHITE'))
            screen.blit(using_string, (570, 640))
            using_string = font.render(f'U - использовать предмет', 1, pygame.Color('WHITE'))
            screen.blit(using_string, (570, 730))

        who_helping_string = font.render('Вам помогает:', 1, pygame.Color('WHITE'))
        screen.blit(who_helping_string, (1370, 640))
        if allie_state:
            who_helping_allie_string = font.render(f'{allie_name.upper()}', 1, pygame.Color('WHITE'))
            screen.blit(who_helping_allie_string, (1370, 730))
        else:
            who_helping_allie_string = font.render(f'Никто :)', 1, pygame.Color('WHITE'))
            screen.blit(who_helping_allie_string, (1370, 730))

    victory = False
    count_flag = 1000
    battle_running = True
    while battle_running and count_flag > 0:
        # print('count game_screen = ' + str(count_flag))
        # count_flag -= 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # print('165')
                battle_running = False
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not battle_in_progress:
                        if not victory:
                            battle(font, is_there_allie, allie, is_there_item, item_name, item)
                            battle_in_progress = True
                if event.key == pygame.K_u:
                    if battle_in_progress:
                        if is_there_item:
                            if not used_item:
                                for i in range(len(item)):
                                    character_mas[i] += item[i]
                                used_item_func()
                                a = 0
                                while a != 3000:
                                    pygame.display.flip()
                                    clock.tick(FPS)
                                    a += 60
                                a = 0
                                battle(font, is_there_allie, allie, is_there_item, item_name, item)
                                used_item = True

                if event.key == pygame.K_a:
                    if character_mas[3] > 0:
                        if who_is_first_bool:
                            dmg_pl = int(character_mas[1] * ((100 - enemy_mas[2]) / 100) + randint(-2, 2))
                            enemy_mas[0] -= dmg_pl
                            who_is_first_bool = 0
                            attacked_func(dmg_pl)
                            c = 0
                            while c != 3000:
                                pygame.display.flip()
                                clock.tick(FPS)
                                c += 60
                            c = 0
                            battle(font, is_there_allie, allie, is_there_item, item_name, item)
                        else:
                            dmg_enemy = int(enemy_mas[1] * ((100 - character_mas[2]) / 100) + randint(-2, 2))
                            character_mas[0] -= dmg_enemy
                            who_is_first_bool = 1
                            being_attacked_func(dmg_enemy)
                            d = 0
                            while d != 6000:
                                pygame.display.flip()
                                clock.tick(FPS)
                                d += 60
                            d = 0
                            battle(font, is_there_allie, allie, is_there_item, item_name, item)
                        if character_mas[0] <= 0:
                            game_over()
                            #  return itemmap, [False, room_y, room_x]
                        if enemy_mas[0] <= 0:
                            # itemmap[map_y][map_x][room_y][room_x] = '0'
                            victory = True
                            #  return itemmap, [True, room_y, room_x]
                        character_mas[3] -= randint(1, 3)
                        if character_mas[3] < 0: character_mas[3] = 0
                    else:
                        game_over()
                        #  return itemmap, [False, room_y, room_x]

        if battle_in_progress and not who_is_first_bool_is_showed:
            who_is_first(who_is_first_bool)
            b = 0
            while b != 3000:
                pygame.display.flip()
                clock.tick(FPS)
                b += 60
            b = 0
            battle(font, is_there_allie, allie, is_there_item, item_name, item)
            who_is_first_bool_is_showed = True

        if enemy_mas[0] <= 0:
            return itemmap, [True, room_y, room_x]

        if character_mas[0] <= 0:
            game_over()

        if victory:
            return itemmap, [True, room_y, room_x]
        # else:
        #     return itemmap, [False, room_y, room_x]

        pygame.display.flip()
        clock.tick(FPS)

        # if not victory:
        #     return itemmap, [False, room_y, room_x]


def battle_en(board, y_enemy_attack, x_enemy_attack, item_key, item_number, y_player, x_player, characters, index):
    # print(x, y)
    # is_defeated = [True, y, x]
    is_defeated = [False, 1, 1]
    if board.player_data[6] < 3:
        return is_defeated, board.enemies, board.items_map_for_current_level
    board.player_data[6] = 0
    if ((board.items_map_for_current_level[board.current_room_y][board.current_room_x][y_player + 1][
             x_player] == f'{item_key}') +
            (board.items_map_for_current_level[board.current_room_y][board.current_room_x][y_player - 1][
                 x_player] == f'{item_key}') +
            (board.items_map_for_current_level[board.current_room_y][board.current_room_x][y_player][
                 x_player + 1] == f'{item_key}') +
            (board.items_map_for_current_level[board.current_room_y][board.current_room_x][y_player][
                 x_player - 1] == f'{item_key}') > 1):
        #  print('2 attack')
        # is_defeated = [False, 0, 0]
        game_over()
    else:
        # for key in board.enemies:
        #     for enemy in board.enemies[key]:
        key = f'{item_key}'
        enemy = board.enemies[key][item_number]
        # if (enemy[-4] == board.current_room_y and enemy[-3] == board.current_room_x and
        #     enemy[-2] == y - 1 and enemy[-1] == x) or (
        #         enemy[-4] == board.current_room_y and enemy[-3] == board.current_room_x and
        #         enemy[-2] == y + 1 and enemy[-1] == x) or (
        #         enemy[-4] == board.current_room_y and enemy[-3] == board.current_room_x and
        #         enemy[-2] == y and enemy[-1] == x - 1) or (
        #         enemy[-4] == board.current_room_y and enemy[-3] == board.current_room_x and
        #         enemy[-2] == y and enemy[-1] == x + 1):
        # if enemy[-4] == board.current_room_y and enemy[-3] == board.current_room_x and enemy[
        #     -2] == y_enemy_attack and enemy[-1] == x_enemy_attack:
        enemy_mas_data = [enemy[0], enemy[1], enemy[2]]
        for key1 in board.allies:
            for allie in board.allies[key1]:
                if allie[-4] == board.current_room_y and allie[-3] == board.current_room_x:
                    is_there_items = False
                    for key2 in board.character_inventory:
                        for type_of_item in board.character_inventory[key2]:
                            if len(type_of_item) != 0:
                                is_there_items = True
                    if is_there_items:
                        flag = True
                        while flag:
                            keyy = randint(70, 76)
                            if len(board.character_inventory[f'{keyy}']) != 0:
                                indexxx = randint(0,
                                                  len(board.character_inventory[
                                                          f'{keyy}']) - 1)
                                if len(board.character_inventory[f'{keyy}'][indexxx]) != 0:
                                    item = board.character_inventory[f'{keyy}'][indexxx][
                                        randint(0, len(
                                            board.character_inventory[f'{keyy}'][
                                                indexxx]) - 1)]
                                    item = board.character_inventory[f'{keyy}'][indexxx]
                                    flag = False
                                else:
                                    continue
                            else:
                                continue
                        item_name_str = board.items[f'{keyy}'][1]
                        board.items_map_for_current_level, is_defeated = battle_screen(
                            board.current_room_y, board.current_room_x,
                            # y - 1,
                            y_player,
                            x_player,
                            board.items_map_for_current_level, characters[index],
                            board.player_data,
                            board.enemies_from_db[key][1],
                            enemy_mas_data, is_there_item=is_there_items,
                            item_name=item_name_str,
                            item=item, is_there_allie=True,
                            allie=board.allies_from_db[key1][1])
                    else:
                        board.items_map_for_current_level, is_defeated = battle_screen(
                            board.current_room_y, board.current_room_x,
                            # y - 1,
                            y_player,
                            x_player,
                            board.items_map_for_current_level, characters[index],
                            board.player_data,
                            board.enemies_from_db[key][1],
                            enemy_mas_data, is_there_allie=True,
                            allie=board.allies_from_db[key1][1])
        is_there_items = False
        for key2 in board.character_inventory:
            for type_of_item in board.character_inventory[key2]:
                if len(type_of_item) != 0:
                    is_there_items = True
        if is_there_items:
            flag = True
            while flag:
                keyy = randint(70, 76)
                if len(board.character_inventory[f'{keyy}']) != 0:
                    indexxx = randint(0,
                                      len(board.character_inventory[f'{keyy}']) - 1)
                    if len(board.character_inventory[f'{keyy}'][indexxx]) != 0:
                        item = board.character_inventory[f'{keyy}'][indexxx][
                            randint(0, len(
                                board.character_inventory[f'{keyy}'][
                                    indexxx]) - 1)]
                        item = board.character_inventory[f'{keyy}'][indexxx]
                        flag = False
                    else:
                        continue
                else:
                    continue
            item_name_str = board.items[f'{keyy}'][1]
            board.items_map_for_current_level, is_defeated = battle_screen(
                board.current_room_y,
                board.current_room_x,
                # y - 1,
                y_player,
                x_player,
                board.items_map_for_current_level,
                characters[index],
                board.player_data,
                board.enemies_from_db[key][1],
                enemy_mas_data,
                is_there_item=is_there_items,
                item_name=item_name_str,
                item=item)
        else:
            board.items_map_for_current_level, is_defeated = battle_screen(
                board.current_room_y,
                board.current_room_x,
                # y - 1,
                y_player,
                x_player,
                board.items_map_for_current_level,
                characters[index],
                board.player_data,
                board.enemies_from_db[key][1],
                enemy_mas_data)

            print_mas = f'{enemy_mas_data[0]} {enemy_mas_data[1]} {enemy_mas_data[2]}'
            #  print(
            #      f'b_s y_player={y_player} x_player={x_player} y_enemie_attack={y_enemy_attack} x_enemie_attack={x_enemy_attack} mas={print_mas}')
            # break

    if is_defeated[0]:
        delta_pos = 0
        # for key in range(40, 45):
        #     # index_enemy = 0
        #     for enemy in range(len(board.enemies[f'{key}'])):
        # y_coord_enemies = board.enemies[f'{key}'][enemy][-2]
        # x_coord_enemies = board.enemies[f'{key}'][enemy][-1]
        key = item_key
        enemy = item_number
        # if is_defeated[-1] - delta_pos <= x_enemy_attack <= is_defeated[-1] + delta_pos and \
        #         is_defeated[-2] - delta_pos <= y_enemy_attack <= is_defeated[-2] + delta_pos:
        #     # print_mas = "\n".join([f'{item[0]} {item[1]} {item[2]} {item[3]} {item[4]} {item[5]}' for item in
        #     #                        board.enemies[f'{key}'][enemy]])
        #     enemy_data = board.enemies[f'{key}'][enemy]
        #     itemmap_current_room = board.items_map_for_current_level[board.current_room_y][board.current_room_x]
        #     print_mas = f'{enemy_data[0]} {enemy_data[1]} {enemy_data[2]} {enemy_data[3]} {enemy_data[4]} {enemy_data[5]} {enemy_data[6]}'
        #     board.enemies[f'{key}'].pop(enemy)
        #     board.items_map_for_current_level[board.current_room_y][board.current_room_x][y_enemy_attack][
        #         x_enemy_attack] = '0'
        #     print(f'убили врага key={key} enemy={enemy} xy={x_player, y_player} mas={print_mas}')
        #     #break
        #         # index_enemy += 1

        enemy_data = board.enemies[f'{key}'][enemy]
        itemmap_current_room = board.items_map_for_current_level[board.current_room_y][board.current_room_x]
        print_mas = f'{enemy_data[0]} {enemy_data[1]} {enemy_data[2]} {enemy_data[3]} {enemy_data[4]} {enemy_data[5]} {enemy_data[6]}'
        board.enemies[f'{key}'].pop(enemy)
        board.items_map_for_current_level[board.current_room_y][board.current_room_x][y_enemy_attack][
            x_enemy_attack] = '0'
        #  print(f'убили врага key={key} enemy={enemy} yx_pl={y_player, x_player} mas={print_mas}')
        # break
        # index_enemy += 1

    # is_defeated[0] = True
    return is_defeated, board.enemies, board.items_map_for_current_level


def find_battle_position(itemmap, enemies, current_room_y, current_room_x, y_player, x_player):
    find_enemies = False
    # print ('player = ', y, x)
    y_enemy_attack = 0
    x_enemy_attack = 0
    item_key = 0
    item_number = 0

    if x_player < 1 or x_player > 25 or y_player < 1 or y_player > 11:
        return find_enemies, y_enemy_attack, x_enemy_attack, item_key, item_number

    itemmap_current_room = itemmap[current_room_y][current_room_x]

    for key in range(40, 45):
        for enemy in range(len(enemies[f'{key}'])):
            y_coord_enemy = enemies[f'{key}'][enemy][-2]
            x_coord_enemy = enemies[f'{key}'][enemy][-1]
            item_key = key
            item_number = enemy

            if itemmap_current_room[y_player + 1][
                x_player] == f'{key}' and y_coord_enemy == y_player + 1 and x_coord_enemy == x_player:
                y_enemy_attack = y_player + 1
                x_enemy_attack = x_player
                find_enemies = True
                #  print('find enemy = ', find_enemies, y_enemy_attack, x_enemy_attack, item_key, item_number)
                break
                # return battle_enemies, y_enemy_attack, x_enemy_attack

            if itemmap_current_room[y_player - 1][
                x_player] == f'{key}' and y_coord_enemy == y_player - 1 and x_coord_enemy == x_player:
                y_enemy_attack = y_player - 1
                x_enemy_attack = x_player
                find_enemies = True
                #  print('find enemy = ', find_enemies, y_enemy_attack, x_enemy_attack, item_key, item_number)
                break
                # return battle_enemies, y_enemy_attack, x_enemy_attack

            if itemmap_current_room[y_player][
                x_player + 1] == f'{key}' and y_coord_enemy == y_player and x_coord_enemy == x_player + 1:
                y_enemy_attack = y_player
                x_enemy_attack = x_player + 1
                find_enemies = True
                #  print('find enemy = ', find_enemies, y_enemy_attack, x_enemy_attack, item_key, item_number)
                break
                # return battle_enemies, y_enemy_attack, x_enemy_attack

            if itemmap_current_room[y_player][
                x_player - 1] == f'{key}' and y_coord_enemy == y_player and x_coord_enemy == x_player - 1:
                y_enemy_attack = y_player
                x_enemy_attack = x_player - 1
                find_enemies = True
                #  print('find enemy = ', find_enemies, y_enemy_attack, x_enemy_attack, item_key, item_number)
                break
                # return battle_enemies, y_enemy_attack, x_enemy_attack

        if find_enemies: break

    return find_enemies, y_enemy_attack, x_enemy_attack, item_key, item_number


def dialog(mas, name, is_this_a_collectible=False):
    pygame.init()

    if not is_this_a_collectible:
        intro_text = [f"Вы взяли {name.upper()},",
                      f"       который увеличил:",
                      "",
                      f"ЗДОРОВЬЕ на {mas[0]}",
                      f"УРОН на {mas[1]}",
                      f"ЗАЩИТУ на {mas[2]}",
                      f"ЭНЕРГИЮ на {mas[3]}",
                      f"УДАЧУ на {mas[4]}"
                      "",
                      "",
                      "  Для продолжения игры, нажмите SPACE"
                      ]
    else:
        intro_text = [f"Вы взяли {name.upper()}, ",
                      f"       c параметрами в битве:",
                      "",
                      f"ЗДОРОВЬЕ +{mas[0]}",
                      f"УРОН +{mas[1]}",
                      f"ЗАЩИТА +{mas[2]}",
                      f"ЭНЕРГИЯ +{mas[3]}",
                      f"УДАЧА +{mas[4]}"
                      "",
                      "",
                      "  Для продолжения игры, нажмите SPACE"
                      ]

    screen.fill((0, 0, 0))
    font = pygame.font.Font('fonts\\Hombre Regular.otf', 60)
    text_coord = 50
    first_letter = True
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('WHITE'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        if first_letter:
            intro_rect.x = 550
            first_letter = False
        else:
            intro_rect.x = 450
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
        pygame.display.flip()
        clock.tick(FPS)


#  board.current_room_x - координата комнаты по иксу, а с y по игреку
# board.player[y][x]
def enemies_moves(dictik, objectmap, itemmap, player, player_coord, current_room_y, current_room_x):
    battle_enemies = False

    for key in dictik:
        if dictik[key]:
            # print(dictik[key])
            for i in range(len(dictik[key])):
                coord_y = dictik[key][i][-2]
                coord_x = dictik[key][i][-1]
                coord_room_y = dictik[key][i][-4]
                coord_room_x = dictik[key][i][-3]
                itemmap_current = itemmap[coord_room_y][coord_room_x]
                # print(len(objectmap), len(objectmap[0]), len(itemmap[coord_room_y][coord_room_x]),
                #      len(itemmap[coord_room_y][coord_room_x][0]))
                flag = True
                enemies_rnd = True
                count_flag = 1000
                while flag and count_flag > 0:
                    count_flag -= 1

                    rnd_x_y = randint(0, 3)  # 0 - вверх, 1 - вправо, 2 - вниз, 3 - влево

                    # враги бегут по направлению к персонажу
                    if enemies_rnd and current_room_y == coord_room_y and current_room_x == coord_room_x:
                        y_player, x_player = player_coord
                        delta_coord_x = coord_x - x_player
                        delta_coord_y = coord_y - y_player
                        if abs(delta_coord_x) > abs(delta_coord_y):
                            if delta_coord_x >= 0:
                                rnd_x_y = 3
                            else:
                                rnd_x_y = 1
                        else:
                            if delta_coord_y >= 0:
                                rnd_x_y = 0
                            else:
                                rnd_x_y = 2
                        enemies_rnd = False

                    # print('=', coord_y, coord_x, rnd_x_y, key)

                    # 0 - вверх
                    if rnd_x_y == 0:
                        if coord_y > 3:
                            if (current_room_y == coord_room_y and current_room_x == coord_room_x) and (
                                    player[coord_y - 1][coord_x] == '5'
                                    or itemmap_current[coord_y - 1][coord_x] == key
                                    or itemmap_current[coord_y - 2][coord_x] == key
                                    or itemmap_current[coord_y - 1][coord_x - 1] == key
                                    or itemmap_current[coord_y - 1][coord_x + 1] == key
                                    or itemmap_current[coord_y - 2][coord_x - 1] == key
                                    or itemmap_current[coord_y - 2][coord_x + 1] == key
                               ):
                                # битва с врагом
                                # print('битва')
                                # battle_enemies = True
                                flag = False
                                continue

                            if objectmap[coord_room_y][coord_room_x][coord_y - 1][coord_x] == '2' and \
                                    itemmap_current[coord_y - 1][coord_x] == '0':
                                # print('-', coord_y - 1, coord_x, rnd_x_y, key)
                                dictik[key][i][-2] -= 1
                                itemmap_current[coord_y - 1][coord_x] = str(key)
                                itemmap_current[coord_y][coord_x] = '0'
                                flag = False
                                continue

                    # 1 - вправо
                    if rnd_x_y == 1:
                        if coord_x < 23:
                            if (current_room_y == coord_room_y and current_room_x == coord_room_x) and (
                                    player[coord_y][coord_x + 1] == '5'
                                    or itemmap_current[coord_y][coord_x + 1] == key
                                    or itemmap_current[coord_y][coord_x + 2] == key
                                    or itemmap_current[coord_y - 1][coord_x + 1] == key
                                    or itemmap_current[coord_y + 1][coord_x + 1] == key
                                    or itemmap_current[coord_y - 1][coord_x + 2] == key
                                    or itemmap_current[coord_y + 1][coord_x + 2] == key
                            ):
                                # битва с врагом
                                # print('битва')
                                # battle_enemies = True
                                flag = False
                                continue
                            # try:
                            if objectmap[coord_room_y][coord_room_x][coord_y][coord_x + 1] == '2' and \
                                    itemmap_current[coord_y][coord_x + 1] == '0':
                                # print('-', coord_y, coord_x + 1, rnd_x_y, key)
                                dictik[key][i][-1] += 1
                                itemmap_current[coord_y][coord_x + 1] = str(key)
                                itemmap_current[coord_y][coord_x] = '0'
                                flag = False
                                continue
                        # except IndexError:
                        #     pass

                    # 2 - вниз
                    if rnd_x_y == 2:
                        if coord_y < 9:
                            if (current_room_y == coord_room_y and current_room_x == coord_room_x) and (
                                    player[coord_y + 1][coord_x] == '5'
                                    or itemmap_current[coord_y + 1][coord_x] == key
                                    or itemmap_current[coord_y + 2][coord_x] == key
                                    or itemmap_current[coord_y + 1][coord_x - 1] == key
                                    or itemmap_current[coord_y + 1][coord_x + 1] == key
                                    or itemmap_current[coord_y + 2][coord_x - 1] == key
                                    or itemmap_current[coord_y + 2][coord_x + 1] == key
                            ):
                                # битва с врагом
                                # print('битва')
                                # battle_enemies = True
                                flag = False
                                continue

                            if objectmap[coord_room_y][coord_room_x][coord_y + 1][coord_x] == '2' and \
                                    itemmap_current[coord_y + 1][coord_x] == '0':
                                # print('-', coord_y + 1, coord_x, rnd_x_y, key)
                                dictik[key][i][-2] += 1
                                itemmap_current[coord_y + 1][coord_x] = str(key)
                                itemmap_current[coord_y][coord_x] = '0'
                                flag = False
                                continue

                    # 3 - влево
                    if rnd_x_y == 3:
                        if coord_x > 3:
                            if (current_room_y == coord_room_y and current_room_x == coord_room_x) and (
                                    player[coord_y][coord_x - 1] == '5'
                                    or itemmap_current[coord_y][coord_x - 1] == key
                                    or itemmap_current[coord_y][coord_x - 2] == key
                                    or itemmap_current[coord_y - 1][coord_x - 1] == key
                                    or itemmap_current[coord_y + 1][coord_x - 1] == key
                                    or itemmap_current[coord_y - 1][coord_x - 2] == key
                                    or itemmap_current[coord_y + 1][coord_x - 2] == key
                            ):
                                # битва с врагом
                                # print('битва')
                                # battle_enemies = True
                                flag = False
                                continue

                            if objectmap[coord_room_y][coord_room_x][coord_y][coord_x - 1] == '2' and \
                                    itemmap_current[coord_y][coord_x - 1] == '0':
                                # print('-', coord_y, coord_x - 1, rnd_x_y, key)
                                dictik[key][i][-1] -= 1
                                itemmap_current[coord_y][coord_x - 1] = str(key)
                                itemmap_current[coord_y][coord_x] = '0'
                                flag = False
                                # continue
    return dictik, itemmap, battle_enemies


def allies_moves(dictik, objectmap, itemmap, player, current_room_y, current_room_x):
    for key in dictik:
        if dictik[key]:
            # print(dictik[key])
            for i in range(len(dictik[key])):
                coord_y = dictik[key][i][-2]
                coord_x = dictik[key][i][-1]
                coord_room_y = dictik[key][i][-4]
                coord_room_x = dictik[key][i][-3]
                # print(len(objectmap), len(objectmap[0]), len(itemmap[coord_room_y][coord_room_x]),
                #      len(itemmap[coord_room_y][coord_room_x][0]))
                flag = True
                count_flag = 1000
                while flag and count_flag > 0:
                    count_flag -= 1

                    rnd_x_y = randint(0, 3)  # 0 - вверх, 1 - вправо, 2 - вниз, 3 - влево
                    # print('=', coord_y, coord_x, rnd_x_y, key)
                    if rnd_x_y == 0:
                        if coord_y > 1:
                            # if coord_y < 2 and 12 <= coord_x <= 14 and objectmap[0][13] == '4':
                            #     dictik[key][i][-4] -= 1
                            #     dictik[key][i][-2] = 11
                            #     dictik[key][i][-1] = 13
                            #     itemmap[coord_room_y - 1][coord_room_x][11][13] = str(key)
                            #     itemmap[coord_room_y][coord_room_x][coord_y][coord_x] = '0'
                            #     flag = False
                            #     continue

                            if (current_room_y == coord_room_y and current_room_x == coord_room_x
                                    and player[coord_y][coord_x - 1] == '5'
                            ):
                                # битва с врагом
                                # print('битва')
                                battle_enemies = True
                                flag = False
                                continue

                            if objectmap[coord_room_y][coord_room_x][coord_y - 1][coord_x] == '2' and \
                                    itemmap[coord_room_y][coord_room_x][coord_y - 1][coord_x] == '0':
                                # print('-', coord_y - 1, coord_x, rnd_x_y, key)
                                dictik[key][i][-2] -= 1
                                itemmap[coord_room_y][coord_room_x][coord_y - 1][coord_x] = str(key)
                                itemmap[coord_room_y][coord_room_x][coord_y][coord_x] = '0'
                                flag = False
                                continue
                    if rnd_x_y == 1:
                        if coord_x < 25:
                            # if 5 <= coord_y <= 7 and coord_x > 24 and objectmap[6][26] == '4':
                            #     dictik[key][i][-3] += 1
                            #     dictik[key][i][-2] = 6
                            #     dictik[key][i][-1] = 1
                            #     itemmap[coord_room_y][coord_room_x + 1][6][1] = str(key)
                            #     itemmap[coord_room_y][coord_room_x][coord_y][coord_x] = '0'
                            #     flag = False
                            #     continue
                            # try:

                            if (current_room_y == coord_room_y and current_room_x == coord_room_x
                                    and player[coord_y][coord_x - 1] == '5'
                            ):
                                # битва с врагом
                                # print('битва')
                                battle_enemies = True
                                flag = False
                                continue

                            if objectmap[coord_room_y][coord_room_x][coord_y][coord_x + 1] == '2' and \
                                    itemmap[coord_room_y][coord_room_x][coord_y][
                                        coord_x + 1] == '0':
                                # print('-', coord_y, coord_x + 1, rnd_x_y, key)
                                dictik[key][i][-1] += 1
                                itemmap[coord_room_y][coord_room_x][coord_y][coord_x + 1] = str(key)
                                itemmap[coord_room_y][coord_room_x][coord_y][coord_x] = '0'
                                flag = False
                                continue
                        # except IndexError:
                        #     pass
                    if rnd_x_y == 2:
                        if coord_y < 11:
                            # if coord_y > 10 and 12 <= coord_x <= 14 and objectmap[12][13] == '4':
                            #     dictik[key][i][-4] += 1
                            #     dictik[key][i][-2] = 1
                            #     dictik[key][i][-1] = 13
                            #     itemmap[coord_room_y + 1][coord_room_x][1][13] = str(key)
                            #     itemmap[coord_room_y][coord_room_x][coord_y][coord_x] = '0'
                            #     flag = False
                            #     continue

                            if (current_room_y == coord_room_y and current_room_x == coord_room_x
                                    and player[coord_y][coord_x - 1] == '5'
                            ):
                                # битва с врагом
                                # print('битва')
                                battle_enemies = True
                                flag = False
                                continue

                            if objectmap[coord_room_y][coord_room_x][coord_y + 1][coord_x] == '2' and \
                                    itemmap[coord_room_y][coord_room_x][coord_y + 1][coord_x] == '0':
                                # print('-', coord_y + 1, coord_x, rnd_x_y, key)
                                dictik[key][i][-2] += 1
                                itemmap[coord_room_y][coord_room_x][coord_y + 1][coord_x] = str(key)
                                itemmap[coord_room_y][coord_room_x][coord_y][coord_x] = '0'
                                flag = False
                                continue
                    if rnd_x_y == 3:
                        if coord_x > 1:
                            # if 5 <= coord_y <= 7 and coord_x < 2 and objectmap[6][0] == '4':
                            #     dictik[key][i][-3] -= 1
                            #     dictik[key][i][-2] = 6
                            #     dictik[key][i][-1] = 25
                            #     itemmap[coord_room_y][coord_room_x - 1][6][25] = str(key)
                            #     itemmap[coord_room_y][coord_room_x][coord_y][coord_x] = '0'
                            #     flag = False
                            #     continue

                            if (current_room_y == coord_room_y and current_room_x == coord_room_x
                                    and player[coord_y][coord_x - 1] == '5'
                            ):
                                # битва с врагом
                                # print('битва')
                                battle_enemies = True
                                flag = False
                                continue

                            if objectmap[coord_room_y][coord_room_x][coord_y][coord_x - 1] == '2' and \
                                    itemmap[coord_room_y][coord_room_x][coord_y][
                                        coord_x - 1] == '0':
                                # print('-', coord_y, coord_x - 1, rnd_x_y, key)
                                dictik[key][i][-1] -= 1
                                itemmap[coord_room_y][coord_room_x][coord_y][coord_x - 1] = str(key)
                                itemmap[coord_room_y][coord_room_x][coord_y][coord_x] = '0'
                                flag = False
                                # continue
    return dictik, itemmap


def main(index, characters):
    #  Инициализируем pygame
    # pygame.init()
    #  Задаём константу, говорящую нам о работе игрового цикла
    running = True
    #  По умолчанию карту мы выводить не будем, поэтому render_map – False
    render_map = False
    render_inventory = False

    #  characters = ['Маг', 'Лесник', 'Шут', 'Анархист']

    #  Инициализируем количество ячеек
    x_cells = 27  # по x
    y_cells = 13  # и по y.
    # Задаём отступы
    left_indent = 46  # слева
    top_indent = 74  # и сверху.
    #  Указываем размер ячейки
    cell_size = 64  # в пикселях.

    steps_without_battle = 10

    player_data = []

    if characters[index] == 'Маг':
        #  Создаём объект персонажа (Маг)
        player = Mage(load_character_from_db(31))
        player_data = player.return_data()
    if characters[index] == 'Лесник':
        player = Forester(load_character_from_db(32))
        player_data = player.return_data()
    if characters[index] == 'Шут':
        player = Fool(load_character_from_db(33))
        player_data = player.return_data()
    if characters[index] == 'Анархист':
        player = Anarchist(load_character_from_db(34))
        player_data = player.return_data()

    #  player_data[1] = 70

    #  Создаём объект игрового поля
    board = board_file.Board(x_cells, y_cells, cell_size, top_indent, left_indent, player_data, characters[index])
    #  Игрок может задавать свои параметры поля
    board.set_view(left_indent, top_indent, cell_size)

    #  Задаём название игры в окне, иконку окна и устанавливаем её
    pygame.display.set_caption('Лес. Нечисть. Русский рок.')
    icon = pygame.image.load('data\\mage_texture_ico.png')
    pygame.display.set_icon(icon)

    #  Загружаем фоновою музыку и ставим её на цикл
    pygame.mixer.music.load('audio/MertviyAnarchist.mp3')
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

    moving_r = moving_d = moving_l = moving_u = False
    animation_image = load_image("room_animation.png")
    animation_x_for_r = animation_y_for_d = -3000
    animation_x_for_l = animation_y_for_u = 3000

    stats_value = 0

    try:
        #  Основной игровой цикл
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                #  При нажатии кнопки M, меняем состояние переменной, которая показывает игроку карту
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        if not render_map:
                            render_map = True
                        else:
                            render_map = False

                    if event.key == pygame.K_i:
                        if not render_inventory:
                            render_inventory = True
                        else:
                            render_inventory = False

                    battle_enemies = False

                    #  При нажатии стрелки вверх, меняем анимацию персонажу, меняем координату персонажу на игровом поле
                    if event.key == pygame.K_UP:

                        board.player_data[6] += 1
                        #  Если текущий спрайт не входит в множество нужных, устанавливаем нужный
                        if board.player_sprite.cur_frame < 4 or board.player_sprite.cur_frame > 6:
                            board.player_sprite.cur_frame = 4
                        #  Далее уже поэтапно увеличиваем фрейм анимации, пока он снова не выйдет за допустимые пределы
                        else:
                            board.player_sprite.cur_frame += 1

                        #  Функцией класса Board находим y и x персонажа на поле
                        y, x = board.return_player_coords()
                        try:
                            #  Смотрим, не пытается ли персонаж переместиться в клетку с препятствием.
                            #  Если нет – меняем координату персонажа
                            # if board.objectmap_for_render[y - 1][x] == '2' and
                            # board.items_map_for_current_level[board.current_room_y][board.current_room_x][y - 1][x] == '0'
                            # and board.room_for_render[y - 1][x] != '1':

                            # if board.objectmap_for_render[y - 1][x] != '3' and (
                            if board.objectmaps_for_current_level[board.current_room_y][board.current_room_x][y - 1][
                                x] != '3' and (
                                    board.items_map_for_current_level[board.current_room_y][board.current_room_x][
                                        y - 1][
                                        x] == '0' or
                                    board.items_map_for_current_level[board.current_room_y][board.current_room_x][
                                        y - 1][
                                        x] in [f'{h}' for h in range(50, 77)]) and board.room_for_render[y - 1][
                                x] != '1':
                                if y - 1 >= 0:
                                    board.player[y][x] = '0'
                                    board.player[y - 1][x] = '5'
                                # Также рассматриваем случаи когда персонаж находится на выходе из комнаты
                                else:
                                    moving_u = True
                                    board.current_room_y -= 1
                                    board.player[y][x] = '0'
                                    board.player[y_cells - 1][x] = '5'
                            # Точно так же и тут, рассматриваем случаи когда персонаж находится на выходе из комнаты
                            elif board.objectmap_for_render[y - 1][x] != '3' and board.room_for_render[y - 1][x] == '1':
                                if board.room_for_render[y][x] == '4' and y == 0:
                                    moving_u = True
                                    board.current_room_y -= 1
                                    board.player[y][x] = '0'
                                    board.player[y_cells - 1][x] = '5'
                        # Предотвращаем вылет по индексации списка
                        except IndexError:
                            pass

                        battle_enemies = False
                        find_enemy, y_enemy_attack, x_enemy_attack, item_key, item_number = find_battle_position(
                            board.items_map_for_current_level,
                            board.enemies,
                            board.current_room_y,
                            board.current_room_x,
                            y, x)
                        if find_enemy:
                            is_defeated, board.enemies, board.items_map_for_current_level = battle_en(board,
                                                                                                      y_enemy_attack,
                                                                                                      x_enemy_attack,
                                                                                                      item_key,
                                                                                                      item_number,
                                                                                                      y, x,
                                                                                                      characters, index)
                            # if not(is_defeated[1] == 0): game_over()
                            #  print(is_defeated[0], y_enemy_attack, x_enemy_attack)

                        board.enemies, board.items_map_for_current_level, battle_enemies = enemies_moves(board.enemies,
                                                                                                         board.objectmaps_for_current_level,
                                                                                                         board.items_map_for_current_level,
                                                                                                         board.player,
                                                                                                         board.return_player_coords(),
                                                                                                         board.current_room_y,
                                                                                                         board.current_room_x)
                        board.allies, board.items_map_for_current_level = allies_moves(board.allies,
                                                                                       board.objectmaps_for_current_level,
                                                                                       board.items_map_for_current_level,
                                                                                       board.player,
                                                                                       board.current_room_y,
                                                                                       board.current_room_x)

                        if not render_map and not render_inventory:
                            board.game_render(screen)  # выводим игру
                        pygame.display.flip()

                        battle_enemies = False
                        find_enemy, y_enemy_attack, x_enemy_attack, item_key, item_number = find_battle_position(
                            board.items_map_for_current_level,
                            board.enemies,
                            board.current_room_y,
                            board.current_room_x,
                            y, x)
                        if find_enemy:
                            is_defeated, board.enemies, board.items_map_for_current_level = battle_en(board,
                                                                                                      y_enemy_attack,
                                                                                                      x_enemy_attack,
                                                                                                      item_key,
                                                                                                      item_number,
                                                                                                      y, x,
                                                                                                      characters, index)
                            # if not(is_defeated[0]): game_over()
                            #  print(is_defeated[0], y_enemy_attack, x_enemy_attack)

                        # if battle_enemies:
                        #     is_defeated, board.enemies, board.items_map_for_current_level = battle_en(board, x, y,
                        #                                                                               characters, index)
                        #     if not(is_defeated[1] == 0): game_over()
                        # battle_enemies = False

                    # При перемещении вниз и вправо нам уже нет необходимости рассматривать дополнительные случаи
                    # Далее по аналогии с перемещением по стрелочке вверх
                    if event.key == pygame.K_DOWN:

                        board.player_data[6] += 1

                        if board.player_sprite.cur_frame > 2:
                            board.player_sprite.cur_frame = 0
                        else:
                            board.player_sprite.cur_frame += 1

                        y, x = board.return_player_coords()
                        try:
                            # if board.objectmap_for_render[y + 1][x] == '2' and
                            # board.items_map_for_current_level[board.current_room_y][board.current_room_x][y + 1][x]
                            # == '0' and board.room_for_render[y + 1][x] != '1':

                            # if board.objectmap_for_render[y + 1][x] != '3' and (
                            if board.objectmaps_for_current_level[board.current_room_y][board.current_room_x][y + 1][
                                x] != '3' and (
                                    board.items_map_for_current_level[board.current_room_y][board.current_room_x][
                                        y + 1][
                                        x] == '0' or
                                    board.items_map_for_current_level[board.current_room_y][board.current_room_x][
                                        y + 1][
                                        x] in [f'{h}' for h in range(50, 77)]) and board.room_for_render[y + 1][
                                x] != '1':
                                board.player[y][x] = '0'
                                board.player[y + 1][x] = '5'
                        #  Примечательно, что при перемещении вниз и вправо, благодаря исключению ошибки на индексацию,
                        #  мы можем избежать дополнительных проверок
                        except IndexError:
                            moving_d = True
                            board.player[y][x] = '0'
                            board.player[0][x] = '5'
                            board.current_room_y += 1

                        battle_enemies = False
                        find_enemy, y_enemy_attack, x_enemy_attack, item_key, item_number = find_battle_position(
                            board.items_map_for_current_level,
                            board.enemies,
                            board.current_room_y,
                            board.current_room_x,
                            y, x)
                        if find_enemy:
                            is_defeated, board.enemies, board.items_map_for_current_level = battle_en(board,
                                                                                                      y_enemy_attack,
                                                                                                      x_enemy_attack,
                                                                                                      item_key,
                                                                                                      item_number,
                                                                                                      y, x,
                                                                                                      characters, index)
                            # if not(is_defeated[1] == 0): game_over()
                            #  print(is_defeated[0], y_enemy_attack, x_enemy_attack)

                        board.enemies, board.items_map_for_current_level, battle_enemies = enemies_moves(board.enemies,
                                                                                                         board.objectmaps_for_current_level,
                                                                                                         board.items_map_for_current_level,
                                                                                                         board.player,
                                                                                                         board.return_player_coords(),
                                                                                                         board.current_room_y,
                                                                                                         board.current_room_x)
                        board.allies, board.items_map_for_current_level = allies_moves(board.allies,
                                                                                       board.objectmaps_for_current_level,
                                                                                       board.items_map_for_current_level,
                                                                                       board.player,
                                                                                       board.current_room_y,
                                                                                       board.current_room_x)

                        if not render_map and not render_inventory:
                            board.game_render(screen)  # выводим игру
                        pygame.display.flip()

                        battle_enemies = False
                        find_enemy, y_enemy_attack, x_enemy_attack, item_key, item_number = find_battle_position(
                            board.items_map_for_current_level,
                            board.enemies,
                            board.current_room_y,
                            board.current_room_x,
                            y, x)
                        if find_enemy:
                            is_defeated, board.enemies, board.items_map_for_current_level = battle_en(board,
                                                                                                      y_enemy_attack,
                                                                                                      x_enemy_attack,
                                                                                                      item_key,
                                                                                                      item_number,
                                                                                                      y, x,
                                                                                                      characters, index)
                            # if not(is_defeated[1] == 0): game_over()
                            #  print(is_defeated[0], y_enemy_attack, x_enemy_attack)

                        # if battle_enemies:
                        #     is_defeated, board.enemies, board.items_map_for_current_level = battle_en(board, x, y,
                        #                                                                               characters, index)
                        #     if is_defeated[1] == 0: game_over()
                        # battle_enemies = False

                    if event.key == pygame.K_RIGHT:

                        board.player_data[6] += 1

                        if board.player_sprite.cur_frame < 12 or board.player_sprite.cur_frame > 14:
                            board.player_sprite.cur_frame = 12
                        else:
                            board.player_sprite.cur_frame += 1

                        y, x = board.return_player_coords()
                        try:
                            # if board.objectmap_for_render[y][x + 1] == '2' and
                            # board.items_map_for_current_level[board.current_room_y][board.current_room_x][y][x + 1] == '0'
                            # and board.room_for_render[y][x + 1] != '1':

                            # if board.objectmap_for_render[y][x + 1] != '3' and (
                            if board.objectmaps_for_current_level[board.current_room_y][board.current_room_x][y][
                                x + 1] != '3' and (
                                    board.items_map_for_current_level[board.current_room_y][board.current_room_x][y][
                                        x + 1] == '0' or
                                    board.items_map_for_current_level[board.current_room_y][board.current_room_x][y][
                                        x + 1] in [f'{h}' for h in range(50, 77)]) and board.room_for_render[y][
                                x + 1] != '1':
                                board.player[y][x] = '0'
                                board.player[y][x + 1] = '5'
                        except IndexError:
                            moving_r = True
                            board.player[y][x] = '0'
                            board.player[y][0] = '5'
                            board.current_room_x += 1

                        battle_enemies = False
                        find_enemy, y_enemy_attack, x_enemy_attack, item_key, item_number = find_battle_position(
                            board.items_map_for_current_level,
                            board.enemies,
                            board.current_room_y,
                            board.current_room_x,
                            y, x)
                        if find_enemy:
                            is_defeated, board.enemies, board.items_map_for_current_level = battle_en(board,
                                                                                                      y_enemy_attack,
                                                                                                      x_enemy_attack,
                                                                                                      item_key,
                                                                                                      item_number,
                                                                                                      y, x,
                                                                                                      characters, index)
                            # if not(is_defeated[1] == 0): game_over()
                            #  print(is_defeated[0], y_enemy_attack, x_enemy_attack)

                        board.enemies, board.items_map_for_current_level, battle_enemies = enemies_moves(board.enemies,
                                                                                                         board.objectmaps_for_current_level,
                                                                                                         board.items_map_for_current_level,
                                                                                                         board.player,
                                                                                                         board.return_player_coords(),
                                                                                                         board.current_room_y,
                                                                                                         board.current_room_x)
                        board.allies, board.items_map_for_current_level = allies_moves(board.allies,
                                                                                       board.objectmaps_for_current_level,
                                                                                       board.items_map_for_current_level,
                                                                                       board.player,
                                                                                       board.current_room_y,
                                                                                       board.current_room_x)

                        if not render_map and not render_inventory:
                            board.game_render(screen)  # выводим игру
                        pygame.display.flip()

                        battle_enemies = False
                        find_enemy, y_enemy_attack, x_enemy_attack, item_key, item_number = find_battle_position(
                            board.items_map_for_current_level,
                            board.enemies,
                            board.current_room_y,
                            board.current_room_x,
                            y, x)
                        if find_enemy:
                            is_defeated, board.enemies, board.items_map_for_current_level = battle_en(board,
                                                                                                      y_enemy_attack,
                                                                                                      x_enemy_attack,
                                                                                                      item_key,
                                                                                                      item_number,
                                                                                                      y, x,
                                                                                                      characters, index)
                            # if not(is_defeated[1] == 0): game_over()
                            #  print(is_defeated[0], y_enemy_attack, x_enemy_attack)

                        # if battle_enemies:
                        #     is_defeated, board.enemies, board.items_map_for_current_level = battle_en(board, x, y,
                        #                                                                               characters, index)
                        #     if is_defeated[1] == 0: game_over()
                        # battle_enemies = False

                    if event.key == pygame.K_LEFT:

                        board.player_data[6] += 1

                        if board.player_sprite.cur_frame < 8 or board.player_sprite.cur_frame > 10:
                            board.player_sprite.cur_frame = 8
                        else:
                            board.player_sprite.cur_frame += 1

                        y, x = board.return_player_coords()
                        try:
                            # if board.objectmap_for_render[y][x - 1] == '2' and
                            # board.items_map_for_current_level[board.current_room_y][board.current_room_x][y][x - 1] == '0'
                            # and board.room_for_render[y][x - 1] != '1':

                            # if board.objectmap_for_render[y][x - 1] != '3' and (
                            if board.objectmaps_for_current_level[board.current_room_y][board.current_room_x][y][
                                x - 1] != '3' and (
                                    board.items_map_for_current_level[board.current_room_y][board.current_room_x][y][
                                        x - 1] == '0' or
                                    board.items_map_for_current_level[board.current_room_y][board.current_room_x][y][
                                        x - 1] in [f'{h}' for h in range(50, 77)]) and board.room_for_render[y][
                                x - 1] != '1':
                                if x - 1 >= 0:
                                    board.player[y][x] = '0'
                                    board.player[y][x - 1] = '5'
                                else:
                                    moving_l = True
                                    board.current_room_x -= 1
                                    board.player[y][x] = '0'
                                    board.player[y][x_cells - 1] = '5'
                            elif board.objectmap_for_render[y][x - 1] != '3' and board.room_for_render[y][x - 1] == '1':
                                if board.room_for_render[y][x] == '4' and x == 0:
                                    moving_l = True
                                    board.current_room_x -= 1
                                    board.player[y][x] = '0'
                                    board.player[y][x_cells - 1] = '5'

                        except Exception as e:
                            print(f"Ошибка: {str(e)}")
                        # except IndexError:
                        #     pass

                        battle_enemies = False
                        find_enemy, y_enemy_attack, x_enemy_attack, item_key, item_number = find_battle_position(
                            board.items_map_for_current_level,
                            board.enemies,
                            board.current_room_y,
                            board.current_room_x,
                            y, x)
                        if find_enemy:
                            is_defeated, board.enemies, board.items_map_for_current_level = battle_en(board,
                                                                                                      y_enemy_attack,
                                                                                                      x_enemy_attack,
                                                                                                      item_key,
                                                                                                      item_number,
                                                                                                      y, x,
                                                                                                      characters, index)
                            # if not(is_defeated[1] == 0): game_over()
                            #  print(is_defeated[0], y_enemy_attack, x_enemy_attack)

                        board.enemies, board.items_map_for_current_level, battle_enemies = enemies_moves(board.enemies,
                                                                                                         board.objectmaps_for_current_level,
                                                                                                         board.items_map_for_current_level,
                                                                                                         board.player,
                                                                                                         board.return_player_coords(),
                                                                                                         board.current_room_y,
                                                                                                         board.current_room_x)
                        board.allies, board.items_map_for_current_level = allies_moves(board.allies,
                                                                                       board.objectmaps_for_current_level,
                                                                                       board.items_map_for_current_level,
                                                                                       board.player,
                                                                                       board.current_room_y,
                                                                                       board.current_room_x)

                        if not render_map and not render_inventory:
                            board.game_render(screen)  # выводим игру
                        pygame.display.flip()

                        battle_enemies = False
                        find_enemy, y_enemy_attack, x_enemy_attack, item_key, item_number = find_battle_position(
                            board.items_map_for_current_level,
                            board.enemies,
                            board.current_room_y,
                            board.current_room_x,
                            y, x)
                        if find_enemy:
                            is_defeated, board.enemies, board.items_map_for_current_level = battle_en(board,
                                                                                                      y_enemy_attack,
                                                                                                      x_enemy_attack,
                                                                                                      item_key,
                                                                                                      item_number,
                                                                                                      y, x,
                                                                                                      characters, index)
                            # if not(is_defeated[1] == 0): game_over()
                            #  print(is_defeated[0], y_enemy_attack, x_enemy_attack)

                        # if battle_enemies:
                        #     is_defeated, board.enemies, board.items_map_for_current_level = battle_en(board, x, y,
                        #                                                                               characters, index)
                        #     if is_defeated[1] == 0: game_over()
                        # battle_enemies = False

            y, x = board.return_player_coords()
            item_id = board.items_map_for_current_level[board.current_room_y][board.current_room_x][y][x]
            if item_id in [f'{j}' for j in range(50, 54)]:
                item_stats = [randint(board.items[item_id][3], board.items[item_id][4]),
                              randint(board.items[item_id][5], board.items[item_id][6]),
                              randint(board.items[item_id][7], board.items[item_id][8]),
                              randint(board.items[item_id][9], board.items[item_id][10]),
                              randint(board.items[item_id][11], board.items[item_id][12])]
                item_name = board.items[item_id][1]
                for i in range(5):
                    board.player_data[i] += item_stats[i]
                board.items_map_for_current_level[board.current_room_y][board.current_room_x][y][x] = '0'
                dialog(item_stats, item_name)

            if item_id in [f'{j}' for j in range(70, 77)]:
                item_stats = [randint(board.items[item_id][3], board.items[item_id][4]),
                              randint(board.items[item_id][5], board.items[item_id][6]),
                              randint(board.items[item_id][7], board.items[item_id][8]),
                              randint(board.items[item_id][9], board.items[item_id][10]),
                              randint(board.items[item_id][11], board.items[item_id][12])]
                item_name = board.items[item_id][1]
                board.character_inventory[item_id].append(item_stats)
                board.items_map_for_current_level[board.current_room_y][board.current_room_x][y][x] = '0'
                dialog(item_stats, item_name, True)

            #  Каждую итерацию игрового цикла обновляем обстановку на экране, заполняя его чёрным
            screen.fill((0, 0, 0))

            #  Если переменная вывода карты не активна
            if not render_map and not render_inventory:
                board.game_render(screen)  # выводим игру
            if render_map:
                board.map_render(screen)  # иначе – карту
            if render_inventory:
                board.inventory_render(screen)

            #  player_data_print = board.player_data

            if (board.game_map[board.current_room_y][
                board.current_room_x] == f'{board.value_of_rooms_int}' and x > 2 and y > 2
                    and x < 25 and y < 11):
                for key1 in board.allies:
                    for allie in board.allies[key1]:
                        if allie[-4] == board.current_room_y and allie[-3] == board.current_room_x:
                            is_there_items = False
                            for key2 in board.character_inventory:
                                for type_of_item in board.character_inventory[key2]:
                                    if len(type_of_item) != 0:
                                        is_there_items = True
                            if is_there_items:
                                flag = True
                                while flag:
                                    keyy = randint(70, 76)
                                    if len(board.character_inventory[f'{keyy}']) != 0:
                                        indexxx = randint(0,
                                                          len(board.character_inventory[
                                                                  f'{keyy}']) - 1)
                                        if len(board.character_inventory[f'{keyy}'][indexxx]) != 0:
                                            item = board.character_inventory[f'{keyy}'][indexxx][
                                                randint(0, len(
                                                    board.character_inventory[f'{keyy}'][
                                                        indexxx]) - 1)]
                                            item = board.character_inventory[f'{keyy}'][indexxx]
                                            flag = False
                                        else:
                                            continue
                                    else:
                                        continue
                                item_name_str = board.items[f'{keyy}'][1]
                                boss_data = board.enemies_from_db['44']
                                boss_data_inp = [randint(boss_data[3],
                                                         boss_data[4]),
                                                 randint(boss_data[5],
                                                         boss_data[6]),
                                                 randint(boss_data[7],
                                                         boss_data[8]),
                                                 board.current_room_y, board.current_room_x, y, x]
                                board.items_map_for_current_level, is_defeated = battle_screen(
                                    board.current_room_y, board.current_room_x, y - 1, x,
                                    board.items_map_for_current_level, characters[index],
                                    board.player_data,
                                    board.enemies_from_db['44'][1], boss_data_inp
                                    , is_there_item=is_there_items,
                                    item_name=item_name_str,
                                    item=item, is_there_allie=True,
                                    allie=board.allies_from_db[key1][1])
                            else:
                                boss_data = board.enemies_from_db['44']
                                boss_data_inp = [randint(boss_data[3],
                                                         boss_data[4]),
                                                 randint(boss_data[5],
                                                         boss_data[6]),
                                                 randint(boss_data[7],
                                                         boss_data[8]),
                                                 board.current_room_y, board.current_room_x, y, x]
                                board.items_map_for_current_level, is_defeated = battle_screen(
                                    board.current_room_y, board.current_room_x, y - 1, x,
                                    board.items_map_for_current_level, characters[index],
                                    board.player_data,
                                    board.enemies_from_db['44'][1],
                                    boss_data_inp, is_there_allie=True,
                                    allie=board.allies_from_db[key1][1])
                is_there_items = False
                for key2 in board.character_inventory:
                    for type_of_item in board.character_inventory[key2]:
                        if len(type_of_item) != 0:
                            is_there_items = True
                if is_there_items:
                    flag = True
                    while flag:
                        keyy = randint(70, 76)
                        if len(board.character_inventory[f'{keyy}']) != 0:
                            indexxx = randint(0,
                                              len(board.character_inventory[f'{keyy}']) - 1)
                            if len(board.character_inventory[f'{keyy}'][indexxx]) != 0:
                                item = board.character_inventory[f'{keyy}'][indexxx][
                                    randint(0, len(
                                        board.character_inventory[f'{keyy}'][
                                            indexxx]) - 1)]
                                item = board.character_inventory[f'{keyy}'][indexxx]
                                flag = False
                            else:
                                continue
                        else:
                            continue
                    item_name_str = board.items[f'{keyy}'][1]
                    boss_data = board.enemies_from_db['44']
                    boss_data_inp = [randint(boss_data[3],
                                             boss_data[4]),
                                     randint(boss_data[5],
                                             boss_data[6]),
                                     randint(boss_data[7],
                                             boss_data[8]),
                                     board.current_room_y, board.current_room_x, y, x]
                    board.items_map_for_current_level, is_defeated = battle_screen(
                        board.current_room_y,
                        board.current_room_x, y - 1,
                        x,
                        board.items_map_for_current_level,
                        characters[index],
                        board.player_data,
                        board.enemies_from_db['44'][1],
                        boss_data_inp,
                        is_there_item=is_there_items,
                        item_name=item_name_str,
                        item=item)
                else:
                    boss_data = board.enemies_from_db['44']
                    boss_data_inp = [randint(boss_data[3],
                                             boss_data[4]),
                                     randint(boss_data[5],
                                             boss_data[6]),
                                     randint(boss_data[7],
                                             boss_data[8]),
                                     board.current_room_y, board.current_room_x, y, x]
                    board.items_map_for_current_level, is_defeated = battle_screen(
                        board.current_room_y,
                        board.current_room_x, y - 1,
                        x,
                        board.items_map_for_current_level,
                        characters[index],
                        board.player_data,
                        board.enemies_from_db['44'][1],
                        boss_data_inp)

                if is_defeated[0]:
                    victory_screen()

            if moving_r:
                animation_x_for_r += 1500

                if animation_x_for_r > 0:
                    animation_x_for_r = -3000
                    moving_r = False

                screen.blit(animation_image, (0, 0))
                pygame.display.flip()

            if moving_d:
                animation_y_for_d += 1500

                if animation_y_for_d > 0:
                    animation_y_for_d = -3000
                    moving_d = False

                screen.blit(animation_image, (0, 0))
                pygame.display.flip()

            if moving_l:
                animation_x_for_l -= 1500

                if animation_x_for_l < 0:
                    animation_x_for_l = 3000
                    moving_l = False

                screen.blit(animation_image, (0, 0))
                pygame.display.flip()

            if moving_u:
                animation_y_for_u -= 1500

                if animation_y_for_u < 0:
                    animation_y_for_u = 3000
                    moving_u = False

                screen.blit(animation_image, (0, 0))
                pygame.display.flip()

            if stats_value % 240 == 0:
                if board.daemon_sprite.cur_frame < 7:
                    board.daemon_sprite.cur_frame += 1
                else:
                    board.daemon_sprite.cur_frame = 0

                if board.skeleton_sprite.cur_frame < 7:
                    board.skeleton_sprite.cur_frame += 1
                else:
                    board.skeleton_sprite.cur_frame = 0

                if board.frogger_sprite.cur_frame < 3:
                    board.frogger_sprite.cur_frame += 1
                else:
                    board.frogger_sprite.cur_frame = 0

            if stats_value > 40000:
                stats_value = 0

            clock.tick(FPS)
            stats_value += FPS

            #  Обновляем кадр в целом
            pygame.display.flip()
            # battle_enemies = False
    except IndexError as exc:
        traceback.print_exc()
        # print(f"Ошибка: {str(e)}")
        terminate()

    pygame.quit()
    sys.exit()


def terminate():
    # print('11132')
    pygame.quit()
    sys.exit()


pygame.init()

pygame.mixer.music.load('audio/ProklyatiyStariyDom1.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)


def start_screen(index):
    # pygame.init()

    #  characters = ['Маг', 'Лесник', 'Шут', 'Анархист']
    characters = ['Шут', 'Анархист', 'Лесник', 'Маг']
    intro_text = ["Лес. Нечисть. Русский рок.",
                  "",
                  "",
                  "",
                  f"Текущий персонаж: {characters[index]}",
                  "Для смены персонажа, нажмите SPACE",
                  "Чтобы начать игру нажмите ENTER"]

    fon = pygame.transform.scale(load_image('background1.png'), size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font('fonts\\Hombre Regular.otf', 60)
    text_coord = 200
    first_letter = True
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('WHITE'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        if first_letter:
            intro_rect.x = 650
            first_letter = False
        else:
            intro_rect.x = 550
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return main(index, characters)
                    #  pygame.mixer.music.stop()
                if event.key == pygame.K_SPACE:
                    if index <= 2:
                        return start_screen(index + 1)
                    else:
                        return start_screen(index - 3)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    start_screen(0)
