class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column




class Ship:
    def __init__(self, start, end, is_drowned=False):
        self.start = start
        self.end = end

    def get_deck(self, row, column):
        # Find the corresponding deck in the list
        pass

    @staticmethod
    def fire(row, column):
        return row, column


class Battleship:
    def __init__(self, ships):
        self.ship = ships
        self.field = {}
        self.make_a_dict_of_ship()
        self.deck = Deck(10, 10)
        self._print_matrix()

    def make_a_dict_of_ship(self):
        list_of_ship = []
        for point in self.ship:
            coord_1 = (point[1][0] - point[0][0])
            coord_2 = (point[1][1] - point[0][1])
            if coord_1 > 0:
                list_of_ship = [(x, point[1][1]) for x in range(point[1][0], point[0][0] - 1, -1)]
            elif coord_2 > 0:
                list_of_ship = [(point[1][0], y) for y in range(point[1][1], point[0][1] - 1, -1)]
            elif coord_1 == 0 and coord_2 == 0:
                list_of_ship.append((point[1][0], point[1][1]))
            self.field[point] = list_of_ship
            list_of_ship = []



    def _print_matrix(self):
        coordik = []
        dict_of_matrix = {}
        for i in range(0, 10, 1):
            for v in range(0, 10, 1):
                coord = (i, v)
                if coord in coordik:
                    dict_of_matrix[coord] = "□"
                else:
                    dict_of_matrix[coord] = "~"
        matrix = [list(dict_of_matrix.values())[i:i + 10] for i in range(0, 100, 10)]
        for row in matrix:
            print(" ".join(str(element) for element in row))

    def fire(self, location: tuple):
        for value in self.field.values():
            for cord in value:
                if location == cord:
                    if len(value) > 1:
                        value.remove(cord)
                        return "Hit!"
                    else:
                        value.remove(cord)
                        return "Sunk!"
        return "Miss!"
