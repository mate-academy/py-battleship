class Deck:
    def __init__(self, row: int, column: int) -> None:
        self.row = row
        self.column = column

    def make_a_deck(self) -> dict:
        dict_of_matrix = {}
        for coord_x in range(0, self.row, 1):
            for coord_y in range(0, self.column, 1):
                dict_of_matrix[(coord_x, coord_y)] = "~"
        return dict_of_matrix


class Battleship:
    def __init__(self, ships: tuple) -> None:
        self.ship = ships
        self.deck = Deck(10, 10).make_a_deck()
        self.field = {}
        self.make_a_dict_of_ship()
        self.table = self._make_symbol_of_table()

    def make_a_dict_of_ship(self) -> None:
        name = 1
        list_of_ship = []
        for point in self.ship:
            coord_1 = (point[1][0] - point[0][0])
            coord_2 = (point[1][1] - point[0][1])
            if coord_1 > 0:
                list_of_ship = [
                    (x, point[1][1]) for x
                    in range(point[1][0], point[0][0] - 1, -1)
                ]
            elif coord_2 > 0:
                list_of_ship = [
                    (point[1][0], y) for y
                    in range(point[1][1], point[0][1] - 1, -1)
                ]
            elif coord_1 == 0 and coord_2 == 0:
                list_of_ship.append((point[1][0], point[1][1]))
            self.field[f"ship_{name}"] = list_of_ship
            name += 1
            list_of_ship = []

    def __make_a_list(self) -> list:
        coordik = []
        for cord in self.field.values():
            for _ in cord:
                coordik.append(_)
        return coordik

    def _make_symbol_of_table(self) -> dict:
        coordik = self.__make_a_list()
        dict_of_matrix = self.deck
        for i in coordik:
            if i in dict_of_matrix.keys():
                dict_of_matrix[i] = "□"
        return dict_of_matrix

    def print_matrix(self) -> None:
        dict_of_matrix = self.table
        matrix = [
            list(dict_of_matrix.values())[i:i + 10]
            for i in range(0, 100, 10)
        ]
        for row in matrix:
            print(" ".join(str(element) for element in row))

    def fire(self, location: tuple) -> str:
        for value in self.field.values():
            for cord in value:
                if location == cord:
                    if len(value) > 1:
                        self.table[location] = "*"
                        value.remove(cord)
                        return "Hit!"
                    else:
                        self.table[location] = "*"
                        value.remove(cord)
                        return "Sunk!"
        self.table[location] = "!"
        return "Miss!"
