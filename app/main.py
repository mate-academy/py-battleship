class Deck:
    def __init__(self, row, column, is_alive=True):
        pass


class Ship:
    def __init__(self, start, end, is_drowned=False):
        # Create decks and save them to a list `self.decks`
        pass

    def get_deck(self, row, column):
        # Find the corresponding deck in the list
        pass

    def fire(self, row, column):
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        pass


class Battleship:
    def __init__(self, ships):
        matrix = [["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                  ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                  ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                  ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                  ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                  ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                  ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                  ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                  ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                  ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"]]
        for ship in ships:
            if ship[0] == ship[1]:
                matrix[ship[0][0]][ship[0][1]] = "□"
            if ship[0][0] != ship[1][0]:
                for length_shipy in range(ship[0][0], ship[1][0] + 1):
                    matrix[length_shipy][ship[1][1]] = "□"
            if ship[0][1] != ship[1][1]:
                for length_shipx in range(ship[0][1], ship[1][1] + 1):
                    matrix[ship[0][0]][length_shipx] = "□"
        self.matrix = matrix
        self.ships = ships

    def fire(self, location: tuple):
        y = location[0]
        x = location[1]
        if y == 9 and x == 9:
            if self.matrix[y][x] == "□" and self.matrix[y][x - 1] != "□" and self.matrix[y - 1][x] != "□":
                self.matrix[y][x] = "X"
                return "Sunk!"
        elif y == 0 and x == 0:
            if self.matrix[y][x] == "□" and self.matrix[y][x + 1] != "□" and self.matrix[y + 1][x] != "□":
                self.matrix[y][x] = "X"
                return "Sunk!"
        elif y == 9 and x == 0:
            if self.matrix[y][x] == "□" and self.matrix[y][x + 1] != "□" and self.matrix[y - 1][x] != "□":
                self.matrix[y][x] = "X"
                return "Sunk!"
        elif y == 0 and x == 9:
            if self.matrix[y][x] == "□" and self.matrix[y][x - 1] != "□" and self.matrix[y + 1][x] != "□":
                self.matrix[y][x] = "X"
                return "Sunk!"
        elif y == 9:
            if self.matrix[y][x] == "□" and self.matrix[y][x + 1] != "□" and self.matrix[y - 1][x] != "□" and self.matrix[y][x - 1] != "□":
                self.matrix[y][x] = "X"
                return "Sunk!"
        elif x == 9:
            if self.matrix[y][x] == "□" and self.matrix[y][x - 1] != "□" and self.matrix[y - 1][x] != "□" and self.matrix[y + 1][x] != "□":
                self.matrix[y][x] = "X"
                return "Sunk!"
        elif self.matrix[y][x] == "□" and self.matrix[y][x + 1] != "□" and self.matrix[y][x - 1] != "□" and self.matrix[y + 1][x] != "□" and self.matrix[y - 1][x] != "□":
            self.matrix[y][x] = "X"
            return "Sunk!"
        elif self.matrix[y][x] == "□":
            self.matrix[y][x] = "*"
            return "Hit!"
        self.matrix[y][x] = "X"
        return "Miss!"
    def __repr__(self):
        result = ""
        for line in self.matrix:
            result += "  ".join(line) + "\n"
        return result
    def _validate_field(self):
        real ={4: 0, 3: 0, 2: 0, 1: 0}
        must_be = {4: 1, 3: 2, 2: 3, 1: 4}
        if len(self.ships) != 10:
            return False
        for ship in self.ships:
            if ship[0] == ship[1]:
                real[1] += 1
            if ship[0][0] != ship[1][0]:
                real[ship[1][0] - ship[0][0] + 1] += 1
            if ship[0][1] != ship[1][1]:
                real[ship[1][1] - ship[0][1] + 1] += 1
        return real == must_be
