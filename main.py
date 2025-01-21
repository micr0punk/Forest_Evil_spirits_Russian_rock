import pygame
import board_file
from characters import Mage


def main():
    #  Инициализируем pygame
    pygame.init()
    #  Задаём константу, говорящую нам о работе игрового цикла
    running = True
    #  По умолчанию карту мы выводить не будем, поэтому render_map – False
    render_map = False

    #  Инициализируем количество ячеек
    x_cells = 27  # по x
    y_cells = 13  # и по y.
    # Задаём отступы
    left_indent = 46  # слева
    top_indent = 74  # и сверху.
    #  Указываем размер ячейки
    cell_size = 64  # в пикселях.

    #  Задаём разрешение игры в пикселях
    size = width_in_pixels, height_in_pixels = 1820, 980

    #  Задаём экран, с которым будем работать
    screen = pygame.display.set_mode(size)

    #  Создаём объект персонажа (Маг)
    player = Mage(1, 'Маг', 1, 13, 6, 100, 4, 10)
    player_data = player.data

    #  Создаём объект игрового поля
    board = board_file.Board(x_cells, y_cells, cell_size, top_indent, left_indent, player_data)
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
                    if board.mage_sprite.cur_frame < 4 or board.mage_sprite.cur_frame > 6:
                        board.mage_sprite.cur_frame = 4
                    #  Далее уже поэтапно увеличиваем фрейм анимации, пока он снова не выйдет за допустимые пределы
                    else:
                        board.mage_sprite.cur_frame += 1

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
                                board.current_room_y -= 1
                                board.player[y][x] = '0'
                                board.player[y_cells - 1][x] = '5'
                        # Точно так же и тут, рассматриваем случаи когда персонаж находится на выходе из комнаты
                        elif board.objectmap_for_render[y - 1][x] != '3' and board.room_for_render[y - 1][x] == '1':
                            if board.room_for_render[y][x] == '4' and y == 0:
                                board.current_room_y -= 1
                                board.player[y][x] = '0'
                                board.player[y_cells - 1][x] = '5'
                    # Предотвращаем вылет по индексации списка
                    except IndexError:
                        pass

                # При перемещении вниз и вправо нам уже нет необходимости рассматривать дополнительные случаи
                # Далее по аналогии с перемещением по стрелочке вверх
                if event.key == pygame.K_DOWN:
                    if board.mage_sprite.cur_frame > 2:
                        board.mage_sprite.cur_frame = 0
                    else:
                        board.mage_sprite.cur_frame += 1

                    y, x = board.return_player_coords()
                    try:
                        if board.objectmap_for_render[y + 1][x] != '3' and board.room_for_render[y + 1][x] != '1':
                            board.player[y][x] = '0'
                            board.player[y + 1][x] = '5'
                    #  Примечательно, что при перемещении вниз и вправо, благодаря исключению ошибки на индексацию,
                    #  мы можем избежать дополнительных проверок
                    except IndexError:
                        board.player[y][x] = '0'
                        board.player[0][x] = '5'
                        board.current_room_y += 1

                if event.key == pygame.K_RIGHT:
                    if board.mage_sprite.cur_frame < 12 or board.mage_sprite.cur_frame > 14:
                        board.mage_sprite.cur_frame = 12
                    else:
                        board.mage_sprite.cur_frame += 1

                    y, x = board.return_player_coords()
                    try:
                        if board.objectmap_for_render[y][x + 1] != '3' and board.room_for_render[y][x + 1] != '1':
                            board.player[y][x] = '0'
                            board.player[y][x + 1] = '5'
                    except IndexError:
                        board.player[y][x] = '0'
                        board.player[y][0] = '5'
                        board.current_room_x += 1

                if event.key == pygame.K_LEFT:
                    if board.mage_sprite.cur_frame < 8 or board.mage_sprite.cur_frame > 10:
                        board.mage_sprite.cur_frame = 8
                    else:
                        board.mage_sprite.cur_frame += 1

                    y, x = board.return_player_coords()
                    try:
                        if board.objectmap_for_render[y][x - 1] != '3' and board.room_for_render[y][x - 1] != '1':
                            if x - 1 >= 0:
                                board.player[y][x] = '0'
                                board.player[y][x - 1] = '5'
                            else:
                                board.current_room_x -= 1
                                board.player[y][x] = '0'
                                board.player[y][x_cells - 1] = '5'
                        elif board.objectmap_for_render[y][x - 1] != '3' and board.room_for_render[y][x - 1] == '1':
                            if board.room_for_render[y][x] == '4' and x == 0:
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

        #  Обновляем кадр в целом
        pygame.display.flip()


if __name__ == '__main__':
    main()
