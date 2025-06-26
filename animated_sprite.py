import pygame

all_sprites = pygame.sprite.Group()


#  Создаём класс, позволяющий нам анимировать спрайты, "нарезая" их состояния из единого файла.
class AnimatedSprite(pygame.sprite.Sprite):
    #  Задаём начальные параметры, которые указываем при создании объекта класса
    #  (изображение, кол-во столбцов, кол-во рядов, размер одного спрайта по x и по y)
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    #  "Режем" файл с анимациями на кусочки по x на y
    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):  # Взяли ряды из параметров класса
            for i in range(columns):  # Взяли столбцы из параметров класса
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    #  При вызове функции обновления меняем текущий кусочек изображения с анимацией
    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
