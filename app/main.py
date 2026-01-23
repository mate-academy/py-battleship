class Deck:
    def __init__(self, row: int = 10,
                 column: int = 10) -> None:
        self.row = row
        self.column = column

    def create_field(self) -> list:
        matrix = [[u"\u007E" for _ in range(self.column)]
                  for _ in range(self.row)]
        return matrix


class Ship:
    def __init__(self, ships: list) -> None:
        self.ship = ships
        self.matrix = Deck().create_field()

    def get_deck(self) -> list:
        for i in range(len(self.ship)):
            cordinats_1 = self.ship[i][0]
            cordinats_2 = self.ship[i][1]
            row_1, column_1 = cordinats_1
            row_2, column_2 = cordinats_2
            if row_1 == row_2:
                for elem in range(column_1, column_2 + 1):
                    self.matrix[row_1][elem] = u"\u25A1"
            if column_1 == column_2:
                for elem in range(row_1, row_2 + 1):
                    self.matrix[elem][column_1] = u"\u25A1"
        return self.matrix


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ship = ships
        self.matrix = Ship(ships).get_deck()
        self.dict = self.ship_hit()

    def fire(self, kord: tuple) -> str:
        x, y = kord
        if self.matrix[x][y] == u"\u25A1":
            self.matrix[x][y] = "*"
            for i in self.dict:
                if kord in self.dict[i]:
                    self.dict[i].remove(kord)
                    if self.dict[i] == []:
                        return "Sunk!"
                    return "Hit!"
        else:
            return "Miss!"

    def ship_hit(self) -> dict:
        res = {}
        for i in self.ship:
            sl = []
            if i[0][0] == i[1][0]:
                for elem in range(i[0][1], i[1][1] + 1):
                    sl.append((i[0][0], elem))
            res[i] = sl
        return res
