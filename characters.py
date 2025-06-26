from random import randint


class Mage:
    def __init__(self, stats):
        self.data = stats
        self.hp = randint(stats[0][3], stats[0][4])
        self.damage = randint(stats[0][5], stats[0][6])
        self.protection = randint(stats[0][7], stats[0][8])
        self.energy = randint(stats[0][9], stats[0][10])
        self.luck = randint(stats[0][11], stats[0][12])
        self.id = 31
        self.steps_without_battle = 10

    def return_data(self):
        return [self.hp, self.damage, self.protection, self.energy, self.luck, self.id, self.steps_without_battle]


class Forester:
    def __init__(self, stats):
        self.data = stats
        self.hp = randint(stats[0][3], stats[0][4])
        self.damage = randint(stats[0][5], stats[0][6])
        self.protection = randint(stats[0][7], stats[0][8])
        self.energy = randint(stats[0][9], stats[0][10])
        self.luck = randint(stats[0][11], stats[0][12])
        self.id = 32
        self.steps_without_battle = 10

    def return_data(self):
        return [self.hp, self.damage, self.protection, self.energy, self.luck, self.id, self.steps_without_battle]


class Fool:
    def __init__(self, stats):
        self.data = stats
        self.hp = randint(stats[0][3], stats[0][4])
        self.damage = randint(stats[0][5], stats[0][6])
        self.protection = randint(stats[0][7], stats[0][8])
        self.energy = randint(stats[0][9], stats[0][10])
        self.luck = randint(stats[0][11], stats[0][12])
        self.id = 33
        self.steps_without_battle = 10

    def return_data(self):
        return [self.hp, self.damage, self.protection, self.energy, self.luck, self.id, self.steps_without_battle]


class Anarchist:
    def __init__(self, stats):
        self.data = stats
        self.hp = randint(stats[0][3], stats[0][4])
        self.damage = randint(stats[0][5], stats[0][6])
        self.protection = randint(stats[0][7], stats[0][8])
        self.energy = randint(stats[0][9], stats[0][10])
        self.luck = randint(stats[0][11], stats[0][12])
        self.id = 34
        self.steps_without_battle = 10

    def return_data(self):
        return [self.hp, self.damage, self.protection, self.energy, self.luck, self.id, self.steps_without_battle]
