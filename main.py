import pygame
import board_file
from characters import Mage


def main():
    pygame.init()
    running = True
    render_map = False

    width = 27
    height = 13
    left = 46
    top = 74
    cell_size = 64

    size = width_ww, height_ww = 1820, 980

    screen = pygame.display.set_mode(size)

    player = Mage(1, 'Маг', 1, 13, 6, 100, 4, 10)

    player_data = player.data

    board = board_file.Board(width, height, cell_size, top, left, player_data)
    board.set_view(left, top, cell_size)

    pygame.display.set_caption('Лес. Нечисть. Русский рок.')
    icon = pygame.image.load('data\\mage_texture2.png')
    pygame.display.set_icon(icon)

    pygame.mixer.music.load('audio/MertviyAnarchist.mp3')
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    if not render_map:
                        render_map = True
                    else:
                        render_map = False

                if event.key == pygame.K_UP:
                    y, x = board.return_player_coords()
                    try:
                        if board.objectmap_for_render[y - 1][x] != '3' and board.room_for_render[y - 1][x] != '1':
                            if y - 1 >= 0:
                                board.player[y][x] = '0'
                                board.player[y - 1][x] = '5'
                            else:
                                board.current_room_y -= 1
                                board.player[y][x] = '0'
                                board.player[height - 1][x] = '5'
                        elif board.objectmap_for_render[y - 1][x] != '3' and board.room_for_render[y - 1][x] == '1':
                            if board.room_for_render[y][x] == '4' and y == 0:
                                board.current_room_y -= 1
                                board.player[y][x] = '0'
                                board.player[height - 1][x] = '5'
                    except IndexError:
                        pass

                if event.key == pygame.K_DOWN:
                    y, x = board.return_player_coords()
                    try:
                        if board.objectmap_for_render[y + 1][x] != '3' and board.room_for_render[y + 1][x] != '1':
                            board.player[y][x] = '0'
                            board.player[y + 1][x] = '5'
                    except IndexError:
                        board.player[y][x] = '0'
                        board.player[0][x] = '5'
                        board.current_room_y += 1

                if event.key == pygame.K_RIGHT:
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
                    y, x = board.return_player_coords()
                    try:
                        if board.objectmap_for_render[y][x - 1] != '3' and board.room_for_render[y][x - 1] != '1':
                            if x - 1 >= 0:
                                board.player[y][x] = '0'
                                board.player[y][x - 1] = '5'
                            else:
                                board.current_room_x -= 1
                                board.player[y][x] = '0'
                                board.player[y][width - 1] = '5'
                        elif board.objectmap_for_render[y][x - 1] != '3' and board.room_for_render[y][x - 1] == '1':
                            if board.room_for_render[y][x] == '4' and x == 0:
                                board.current_room_x -= 1
                                board.player[y][x] = '0'
                                board.player[y][width - 1] = '5'

                    except IndexError:
                        pass

        screen.fill((0, 0, 0))
        if not render_map:
            board.new_render(screen, width, height)
        else:
            board.map_render(screen)

        player_data_print = board.player_data

        pygame.display.flip()


if __name__ == '__main__':
    main()
