class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive



class Ship:

    def __init__(self, start, end, is_drowned=False):
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        self.decks_in_list = []

    def decks_list(self):
        if self.start[0] == self.end[0] and self.start[1] != self.end[1]:
            for column_ in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], column_))
        if self.start[1] == self.end[1] and self.start[0] != self.end[0]:
            for row_ in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(row_, self.end[1]))
        if self.start[0] == self.end[0] and self.start[1] == self.end[1]:
            self.decks.append(Deck(self.start[0], self.end[1]))
        return self.decks

    # coздайтке список self.deck
    # Найдите соответствующую колоду в списке
    # Изменяем статус `is_alive` колоды
    # И обновить значение `is_drown`, если это необходимо

    def get_deck(self, row, column):
        for object_ in self.decks:
            if object_.row == row and object_.column == column:
                object_.is_alive = False
                return object_

    def fire(self, row, column):
        obj_deck = self.get_deck(row, column)
        print(obj_deck.is_alive)
        self.decks_in_list.append(obj_deck)
        if len(self.decks) == len(self.decks_in_list):

            return True
        return False




class Battleship:
    def __init__(self, ships):
        self.ships = ships

        self.field = {}
        self.battle_ship = None
        self.padded_decks = []
        self.field_battle()

    def field_battle(self):
        for ship in self.ships:
            if ship[0][0] == ship[1][0] and ship[0][1] != ship[1][1]:
                for column_ in range(ship[0][1], ship[1][1] + 1):
                    self.field[(ship[0][0], column_)] = Ship(ship[0], ship[1])
            if ship[0][1] == ship[1][1] and ship[0][0] != ship[1][0]:
                for row_ in range(ship[0][0], ship[1][0] + 1):
                    self.field[(row_, ship[0][1])] = Ship(ship[0], ship[1])
            if ship[0][0] == ship[1][0] and ship[0][1] == ship[1][1]:
                self.field[(ship[0][0], ship[0][1])] = Ship(ship[0], ship[1])
        # print(self.field)
        return self.field

    def fire(self, location: tuple):

        self.print_field()
        if (location[0], location[1]) not in self.field:  # verify self.field_battle()
            print("Missssssssss")
            return "Miss!"

        ship_object = self.field[location]
        ship_object.decks_list()
        ship_object_true = ship_object.fire(location[0], location[1])
        if (location[0], location[1]) in self.field \
                and self.battle_ship[location[0]][location[1]] == u"\u25A1" and ship_object_true:
            if self.field[location] == ship_object:
                self.padded_decks.append(location)
            print(self.padded_decks)
            self.battle_ship[location[0]][location[1]] = 'x'
            print('\n'.join('\t'.join(map(str, row)) for row in self.battle_ship))
            return "Sunk!"
        if (location[0], location[1]) in self.field \
                and self.battle_ship[location[0]][location[1]] == u"\u25A1":
            self.battle_ship[location[0]][location[1]] = '*'

        print('\n'.join('\t'.join(map(str, row)) for row in self.battle_ship))
        return "Hit!"

    def print_field(self):
        battle_ = [['~'] * 10 for i in range(10)]
        decks_on_field = []
        for key in self.field:    # verify self.field_battle()
            decks_on_field.append(key)
        for row, column in decks_on_field:
            battle_[row][column] = u"\u25A1"
        self.battle_ship = battle_
        return self.battle_ship


battle_ship = Battleship(
    [
        ((0, 0), (0, 3)),
        ((0, 5), (0, 6)),
        ((0, 8), (0, 9)),
        ((2, 0), (4, 0)),
        ((2, 4), (2, 6)),
        ((2, 8), (2, 9)),
        ((9, 9), (9, 9)),
        ((7, 7), (7, 7)),
        ((7, 9), (7, 9)),
        ((9, 7), (9, 7)),
    ],
)

# ship_x = Ship((0, 0), (0, 3))
# print(battle_ship.field_battle())
#deck_obj = Deck(0, 2)
#print(deck_obj.row)
print(battle_ship.fire((0, 4)), battle_ship.fire((0, 5)), battle_ship.fire((0, 2)), battle_ship.fire((0, 1)), battle_ship.fire((0, 0)))
# print(ship_x.decks_in_ships())
# print(battle_ship.print_field())
# print(ship_x.pnt_gf())
# deck_41 = Deck(0, 0)
# deck_44 = Deck(0, 3)
# ship_41 = Ship(deck_41, deck_44)
# deck_31 = Deck(2, 0)
# deck_33 = Deck(4, 0)
# ship_31 = Ship(deck_31, deck_33)
# deck_21 = Deck(0, 5)
# deck_22 = Deck(0, 6)
# ship_21 = Ship(deck_21, deck_22)
# deck_11 = Deck(9, 7)
# ship_11 = Ship(deck_11, deck_11)


# coздайтке список self.deck
# Найдите соответствующую колоду в списке
# Изменяем статус `is_alive` колоды
# И обновить значение `is_drown`, если это необходимо
# Создать словарь `self.field`.
# Его ключами являются кортежи - координаты непустых ячеек,
# Значение для каждой ячейки является ссылкой на корабль который находится в нем

# Эта функция должна проверять, является ли местоположение является ключом в `self.field`
# Если это так, то он должен проверить, является ли эта ячейка последней живой в корабле или нет.
# Если вызывается метод огня, он должен возвращать одну из следующих строк:
# "Miss!" - когда в данной ячейке нет корабля
# "Hit!" - когда в потолке есть колода, но у соответствующего корабля еще есть живая колода
# "Sunk!" - когда остается последняя живая колода.
# Use * for hit decks of the alive ship
# Use x for decks of the drowned ship
