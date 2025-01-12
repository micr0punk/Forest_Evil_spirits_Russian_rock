class Mage:
    def __init__(self, id, name, map_number, room_x, room_y, hp, damage, energy):
        self.data = [id, name, map_number, room_x, room_y, hp, damage, energy]

    def data(self):
        return self.data
