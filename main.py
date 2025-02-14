import sys

import pygame
import board_file
from characters import Mage, Forester, Fool, Anarchist
from database_file import load_character_from_db
from load_image_file import load_image

FPS = 20

#  Задаём разрешение игры в пикселях
size = width_in_pixels, height_in_pixels = 1820, 980

#  Задаём экран, с которым будем работать
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()


def main(index, characters):
    #  Инициализируем pygame
    pygame.init()
    #  Задаём константу, говорящую нам о работе игрового цикла
    running = True
    #  По умолчанию карту мы выводить не будем, поэтому render_map – False
    render_map = False

    #  characters = ['Маг', 'Лесник', 'Шут', 'Анархист']

    #  Инициализируем количество ячеек
    x_cells = 27  # по x
    y_cells = 13  # и по y.
    # Задаём отступы
    left_indent = 46  # слева
    top_indent = 74  # и сверху.
    #  Указываем размер ячейки
    cell_size = 64  # в пикселях.

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

    #  Создаём объект игрового поля
    board = board_file.Board(x_cells, y_cells, cell_size, top_indent, left_indent, player_data, characters[index])
    #  Игрок может задавать свои параметры поля
    board.set_view(left_indent, top_indent, cell_size)

    #  Задаём название игры в окне, иконку окна и устанавливаем её
    pygame.display.set_caption('Лес. Нечисть. Русский рок.')
    icon = pygame.image.load('data\\test assets\\mage_texture2.png')
    pygame.display.set_icon(icon)

    #  Загружаем фоновою музыку и ставим её на цикл
    pygame.mixer.music.load('audio/MertviyAnarchist.mp3')
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

    moving_r = moving_d = moving_l = moving_u = False
    animation_image = load_image("room_animation.png")
    animation_x_for_r = animation_y_for_d = -3000
    animation_x_for_l = animation_y_for_u = 3000

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

                #  При нажатии стрелки вверх, меняем анимацию персонажу, меняем координату персонажу на игровом поле
                if event.key == pygame.K_UP:
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
                        if board.objectmap_for_render[y - 1][x] != '3' and board.room_for_render[y - 1][x] != '1':
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

                # При перемещении вниз и вправо нам уже нет необходимости рассматривать дополнительные случаи
                # Далее по аналогии с перемещением по стрелочке вверх
                if event.key == pygame.K_DOWN:
                    if board.player_sprite.cur_frame > 2:
                        board.player_sprite.cur_frame = 0
                    else:
                        board.player_sprite.cur_frame += 1

                    y, x = board.return_player_coords()
                    try:
                        if board.objectmap_for_render[y + 1][x] != '3' and board.room_for_render[y + 1][x] != '1':
                            board.player[y][x] = '0'
                            board.player[y + 1][x] = '5'
                    #  Примечательно, что при перемещении вниз и вправо, благодаря исключению ошибки на индексацию,
                    #  мы можем избежать дополнительных проверок
                    except IndexError:
                        moving_d = True
                        board.player[y][x] = '0'
                        board.player[0][x] = '5'
                        board.current_room_y += 1

                if event.key == pygame.K_RIGHT:
                    if board.player_sprite.cur_frame < 12 or board.player_sprite.cur_frame > 14:
                        board.player_sprite.cur_frame = 12
                    else:
                        board.player_sprite.cur_frame += 1

                    y, x = board.return_player_coords()
                    try:
                        if board.objectmap_for_render[y][x + 1] != '3' and board.room_for_render[y][x + 1] != '1':
                            board.player[y][x] = '0'
                            board.player[y][x + 1] = '5'
                    except IndexError:
                        moving_r = True
                        board.player[y][x] = '0'
                        board.player[y][0] = '5'
                        board.current_room_x += 1

                if event.key == pygame.K_LEFT:
                    if board.player_sprite.cur_frame < 8 or board.player_sprite.cur_frame > 10:
                        board.player_sprite.cur_frame = 8
                    else:
                        board.player_sprite.cur_frame += 1

                    y, x = board.return_player_coords()
                    try:
                        if board.objectmap_for_render[y][x - 1] != '3' and board.room_for_render[y][x - 1] != '1':
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

                    except IndexError:
                        pass

        #  Каждую итерацию игрового цикла обновляем обстановку на экране, заполняя его чёрным
        screen.fill((0, 0, 0))

        #  Если переменная вывода карты не активна
        if not render_map:
            board.game_render(screen, x_cells, y_cells)  # выводим игру
        else:
            board.map_render(screen)  # иначе – карту

        #  player_data_print = board.player_data

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

        if board.skeleton_sprite.cur_frame < 3:
            board.skeleton_sprite.cur_frame += 1
        else:
            board.skeleton_sprite.cur_frame = 0

        clock.tick(FPS)

        #  Обновляем кадр в целом
        pygame.display.flip()


def terminate():
    pygame.quit()
    sys.exit()

pygame.init()

pygame.mixer.music.load('audio/ProklyatiyStariyDom1.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

def start_screen(index):
    pygame.init()

    #  characters = ['Маг', 'Лесник', 'Шут', 'Анархист']
    characters = ['Шут', 'Анархист', 'Лесник', 'Маг']
    intro_text = ["Лес. Нечисть. Русский рок.",
                  "",
                  "",
                  "",
                  f"Текущий персонаж: {characters[index]}",
                  "Для смены персонажа нажмите SPACE",
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
    start_screen(0)
