from __future__ import annotations


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                return deck

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        for deck in self.decks:
            if deck.is_alive:
                return
        self.is_drowned = True


class Battleship:
    def __init__(self, ships: tuple[tuple]) -> None:
        self.ships = ships
        self.field = {}
        for ship in self.ships:
            ship_obj = Ship(ship[0], ship[1])
            for row in range(ship_obj.start[0], ship_obj.end[0] + 1):
                for column in range(ship_obj.start[1], ship_obj.end[1] + 1):
                    self.field.update({(row, column): ship_obj})
                    ship_obj.decks.append(Deck(row, column))

    def fire(self, location: tuple) -> str:
        if location in self.field:
            self.field[location].fire(location[0], location[1])
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                if (row, column) in self.field:
                    if self.field[(row, column)].is_drowned:
                        print("   x   ", end="")
                    elif not (self.field[(row, column)].
                              get_deck(row, column).
                              is_alive):
                        print("   *   ", end="")
                    else:
                        print("   □   ", end="")
                else:
                    print(end="   ~   ")
            print(end="\n")

    def check_coord_on_desk(self) -> bool:
        for coord in sorted(list(self.field.keys())):
            check_coord_1 = (coord[0] + 1, coord[1])
            if check_coord_1 in self.field:
                if self.field[check_coord_1] is not self.field[coord]:
                    return False
            check_coord_2 = (coord[0], coord[1] + 1)
            if check_coord_2 in self.field:
                if self.field[check_coord_2] is not self.field[coord]:
                    return False
            check_coord_3 = (coord[0] + 1, coord[1] + 1)
            if check_coord_3 in self.field:
                return False
            check_coord_4 = (coord[0] - 1, coord[1] + 1)
            if check_coord_4 in self.field:
                return False
        return True

    def validate_field(self) -> str:
        self.total_ships = len(self.ships)
        self.single_deck, self.double_deck = 0, 0
        self.three_deck, self.four_deck = 0, 0
        for ship in self.ships:
            ship_len = 0
            for row in range(ship[0][0], ship[1][0] + 1):
                for column in range(ship[0][1], ship[1][1] + 1):
                    ship_len += 1
            if ship_len == 1:
                self.single_deck += 1
            elif ship_len == 2:
                self.double_deck += 1
            elif ship_len == 3:
                self.three_deck += 1
            else:
                self.four_deck += 1
        if (self.check_coord_on_desk()
                and self.total_ships == 10
                and self.single_deck == 4
                and self.double_deck == 3
                and self.three_deck == 2
                and self.four_deck == 1):
            return "Validation passed"
        return "Validation not passed"
