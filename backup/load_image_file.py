import pygame
import sys
import os


#  Функция загрузки изображений. Берёт файлы, находящиеся в папке data
def load_image(name, color_key=None):
    fullname = os.path.join('data', name)

    #  Если файла с таким именем нет, оканчиваем работу программы и выводим соответствующее сообщение в консоль
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname)

    #  Добавляем возможность удалять фон с помощью аргумента по умолчанию
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()

    return image
