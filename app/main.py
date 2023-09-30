

class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
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

    def fire(self, location: tuple) -> str:
        y_fire = location[0]
        x_fire = location[1]
        if y_fire == 9 and x_fire == 9:
            if (self.matrix[y_fire][x_fire] == "□"
                    and self.matrix[y_fire][x_fire - 1] != "□"
                    and self.matrix[y_fire - 1][x_fire] != "□"):
                self.matrix[y_fire][x_fire] = "X"
                return "Sunk!"
        elif y_fire == 0 and x_fire == 0:
            if (self.matrix[y_fire][x_fire] == "□"
                    and self.matrix[y_fire][x_fire + 1] != "□"
                    and self.matrix[y_fire + 1][x_fire] != "□"):
                self.matrix[y_fire][x_fire] = "X"
                return "Sunk!"
        elif y_fire == 9 and x_fire == 0:
            if (self.matrix[y_fire][x_fire] == "□"
                    and self.matrix[y_fire][x_fire + 1] != "□"
                    and self.matrix[y_fire - 1][x_fire] != "□"):
                self.matrix[y_fire][x_fire] = "X"
                return "Sunk!"
        elif y_fire == 0 and x_fire == 9:
            if (self.matrix[y_fire][x_fire] == "□"
                    and self.matrix[y_fire][x_fire - 1] != "□"
                    and self.matrix[y_fire + 1][x_fire] != "□"):
                self.matrix[y_fire][x_fire] = "X"
                return "Sunk!"
        elif y_fire == 9:
            if (self.matrix[y_fire][x_fire] == "□"
                    and self.matrix[y_fire][x_fire + 1] != "□"
                    and self.matrix[y_fire - 1][x_fire] != "□"
                    and self.matrix[y_fire][x_fire - 1] != "□"):
                self.matrix[y_fire][x_fire] = "X"
                return "Sunk!"
        elif x_fire == 9:
            if (self.matrix[y_fire][x_fire] == "□"
                    and self.matrix[y_fire][x_fire - 1] != "□"
                    and self.matrix[y_fire - 1][x_fire] != "□"
                    and self.matrix[y_fire + 1][x_fire] != "□"):
                self.matrix[y_fire][x_fire] = "X"
                return "Sunk!"
        elif (self.matrix[y_fire][x_fire] == "□"
              and self.matrix[y_fire][x_fire + 1] != "□"
              and self.matrix[y_fire][x_fire - 1] != "□"
              and self.matrix[y_fire + 1][x_fire] != "□"
              and self.matrix[y_fire - 1][x_fire] != "□"):
            self.matrix[y_fire][x_fire] = "X"
            return "Sunk!"
        elif self.matrix[y_fire][x_fire] == "□":
            self.matrix[y_fire][x_fire] = "*"
            return "Hit!"
        self.matrix[y_fire][x_fire] = "X"
        return "Miss!"

    def __repr__(self) -> str:
        result = ""
        for line in self.matrix:
            result += "  ".join(line) + "\n"
        return result

    def _validate_field(self) -> bool:
        real = {4: 0, 3: 0, 2: 0, 1: 0}
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
