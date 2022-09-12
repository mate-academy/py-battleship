class Battleship:
    empty_field = []
    field_with_ships = []

    def __init__(self, ships: list):
        self.ships = ships

        self.create_empty_field()
        self.filling_the_field_with_ship()

    """Line matrix printing"""

    @staticmethod
    def printer(temp_list: list):
        for i in temp_list:
            pass
        #     print(i)
        # print("")

    """Wrecked ship optimization function"""

    def ship_attacked(self, point: set):
        self.field_with_ships[point[0]][point[1]] = "*"
        self.printer(self.field_with_ships)
        # return print("Hit!\n")
        return "Hit!"

    """Ship sink optimization function"""

    def ship_sunk(self, point: set):
        self.field_with_ships[point[0]][point[1]] = "X"
        for i in range(len(self.field_with_ships)):
            for k in range(len(self.field_with_ships[i])):
                if self.field_with_ships[i][k] == "*":
                    self.field_with_ships[i][k] = "X"
        self.printer(self.field_with_ships)
        # return print("Sunk!\n")
        return "Sunk!"

    """Create an empty field"""

    def create_empty_field(self):

        """Printing an empty field 10x10"""
        self.empty_field = ["~"] * 10
        for i in range(10):
            self.empty_field[i] = ["~"] * 10
        self.printer(self.empty_field)

    """Filling the field with ships"""

    def filling_the_field_with_ship(self):

        for i in range(len(self.ships)):
            x = self.ships[i][1][0] - self.ships[i][0][0]
            y = self.ships[i][1][1] - self.ships[i][0][1]
            if x == 0 and y == 0:
                r = self.ships[i][0][0]
                c = self.ships[i][1][1]
                self.empty_field[r][c] = "\u25A1"
            if x != 0 and y == 0:
                count = 0
                while count != x + 1:
                    r = self.ships[i][0][0] + count
                    c = self.ships[i][0][1]
                    self.empty_field[r][c] = "\u25A1"
                    count += 1
            if x == 0 and y != 0:
                count = 0
                while count != y + 1:
                    r = self.ships[i][0][0]
                    c = self.ships[i][0][1] + count
                    self.empty_field[r][c] = "\u25A1"
                    count += 1
        self.field_with_ships = self.empty_field
        self.printer(self.field_with_ships)

    def fire(self, point: set):

        """Check for misses"""
        if self.field_with_ships[point[0]][point[1]] == "~":
            self.printer(self.field_with_ships)
            # return print("Miss!\n")
            return "Miss!"

        """Checking the central cells"""
        if not point[0] in (0, 9) and not point[1] in (0, 9):
            if self.field_with_ships[point[0]][point[1]] == "\u25A1" \
                    and any((self.field_with_ships[point[0] - 1][point[1]]
                             == "\u25A1",
                             self.field_with_ships[point[0]][point[1] + 1]
                             == "\u25A1",
                             self.field_with_ships[point[0] + 1][point[1]]
                             == "\u25A1",
                             self.field_with_ships[point[0]][point[1] - 1]
                             == "\u25A1")):
                self.ship_attacked(point)
            else:
                self.ship_sunk(point)

        """Checking corner cells"""
        if point[0] in (0, 9) and point[1] in (0, 9):

            """Top left corner"""
            if point[0] == 0 and point[1] == 0:
                if self.field_with_ships[point[0]][point[1]] == "\u25A1" \
                        and any((self.field_with_ships[point[0]][point[1] + 1]
                                 == "\u25A1",
                                 self.field_with_ships[point[0] + 1][point[1]]
                                 == "\u25A1")):
                    self.ship_attacked(point)
                else:
                    self.ship_sunk(point)

            """Top right corner"""
            if point[0] == 0 and point[1] == 9:
                if self.field_with_ships[point[0]][point[1]] == "\u25A1" \
                        and any((self.field_with_ships[point[0] + 1][point[1]]
                                 == "\u25A1",
                                 self.field_with_ships[point[0]][point[1] - 1]
                                 == "\u25A1")):
                    self.ship_attacked(point)
                else:
                    self.ship_sunk(point)

            """Lower left corner"""
            if point[0] == 9 and point[1] == 0:
                if self.field_with_ships[point[0]][point[1]] == "\u25A1" \
                        and any((self.field_with_ships[point[0] - 1][point[1]]
                                 == "\u25A1",
                                 self.field_with_ships[point[0]][point[1] + 1]
                                 == "\u25A1")):
                    self.ship_attacked(point)
                else:
                    self.ship_sunk(point)

            """Lower right corner"""
            if point[0] == 9 and point[1] == 9:
                if self.field_with_ships[point[0]][point[1]] == "\u25A1" \
                        and any((self.field_with_ships[point[0]][point[1] - 1]
                                 == "\u25A1",
                                 self.field_with_ships[point[0] - 1][point[1]]
                                 == "\u25A1")):
                    self.ship_attacked(point)
                else:
                    self.ship_sunk(point)

        self.checking_side_faces_without_corners(point)

        """Checking side faces without corners"""
    def checking_side_faces_without_corners(self, point: set):
        """Upper side"""
        if point[0] == 0 and point[1] in (range(1, 9)):
            if self.field_with_ships[point[0]][point[1]] == "\u25A1" \
                    and any((self.field_with_ships[point[0]][point[1] + 1]
                             == "\u25A1",
                             self.field_with_ships[point[0] + 1][point[1]]
                             == "\u25A1",
                             self.field_with_ships[point[0]][point[1] - 1]
                             == "\u25A1")):
                self.ship_attacked(point)
            else:
                self.ship_sunk(point)

        """Down side"""
        if point[0] == 9 and point[1] in (range(1, 9)):
            if self.field_with_ships[point[0]][point[1]] == "\u25A1" \
                    and any((self.field_with_ships[point[0]][point[1] + 1]
                             == "\u25A1",
                             self.field_with_ships[point[0] - 1][point[1]]
                             == "\u25A1",
                             self.field_with_ships[point[0]][point[1] - 1]
                             == "\u25A1")):
                self.ship_attacked(point)
            else:
                self.ship_sunk(point)

        """Left side"""
        if point[0] in range(1, 9) and point[1] == 0:
            if self.field_with_ships[point[0]][point[1]] == "\u25A1" \
                    and any((self.field_with_ships[point[0] + 1][point[1]]
                             == "\u25A1",
                             self.field_with_ships[point[0] - 1][point[1]]
                             == "\u25A1",
                             self.field_with_ships[point[0]][point[1] + 1]
                             == "\u25A1")):
                self.ship_attacked(point)
            else:
                self.ship_sunk(point)

        """Right side"""
        if point[0] in range(1, 9) and point[1] == 9:
            if self.field_with_ships[point[0]][point[1]] == "\u25A1" \
                    and any((self.field_with_ships[point[0] + 1][point[1]]
                             == "\u25A1",
                             self.field_with_ships[point[0] - 1][point[1]]
                             == "\u25A1",
                             self.field_with_ships[point[0]][point[1] - 1]
                             == "\u25A1")):
                self.ship_attacked(point)
            else:
                self.ship_sunk(point)
