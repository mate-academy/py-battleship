from xml.dom import ValidationErr


class Battleship:
    def __init__(self, ships, field):
        self.field = field
        self.ships = ships

    @property
    def ships(self):
        return self._ships

    @ships.setter
    def ships(self, ships_list):
        if len(ships_list) != 10:
            raise ValueError(f"Count of ships must be equal 10, but got {len(ships_list)}")

        def ship_length(x1, y1, x2, y2):
            return max(abs(x2 - x1), abs(y2 - y1)) + 1

        counts = {1: 0, 2: 0, 3: 0, 4: 0}

        for (x1, y1), (x2, y2) in ships_list:
            length = ship_length(x1, y1, x2, y2)

            if length not in counts:
                raise ValidationErr(f"Invalid ship length: {length}")

            counts[length] += 1

        if counts[1] != 4:
            raise ValidationErr(f"Expected 4 single-deck ships, got {counts[1]}")

        if counts[2] != 3:
            raise ValidationErr(f"Expected 3 double-deck ships, got {counts[2]}")

        if counts[3] != 2:
            raise ValidationErr(f"Expected 2 triple-deck ships, got {counts[3]}")

        if counts[4] != 1:
            raise ValidationErr(f"Expected 1 four-deck ship, got {counts[4]}")

        self._ships = ships_list

        for (x1, y1), (x2, y2) in ships_list:
            if x1 == x2:
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    self.field[x1][y] = u"\u25A1"
            else:
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    self.field[x][y1] = u"\u25A1"


    def fire(self, location: tuple):
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        pass

    def print_field(self):
        for row in self.field:
            print(" ".join(row))