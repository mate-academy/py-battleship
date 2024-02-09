class Deck:
    def __init__(
            self,
            row: int,
            column: int,
            is_alive: bool = True
    ) -> None:
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
        self.srart = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = [
            Deck(row_index, column_index)
            for column_index in range(start[1], end[1] + 1)
            for row_index in range(start[0], end[0] + 1)
        ]

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        if self.get_deck(row, column) is not None:
            self.get_deck(row, column).is_alive = False
            if all(not deck.is_alive for deck in self.decks):
                self.is_drowned = True

    def __len__(self) -> int:
        return len(self.decks)


class Battleship:
    def __init__(
            self,
            ships: list
    ) -> None:
        self.field = {}
        for ship in ships:
            my_ship = Ship(ship[0], ship[1])
            for deck in my_ship.decks:
                self.field[(deck.row, deck.column)] = my_ship
        self.ships = [
            Ship(ship[0], ship[-1])
            for ship in ships
        ]
        self._validate_field()

    def _validate_field(self) -> None:
        conditions = [
            len(self.ships) == 10,
            len([ship for ship in self.ships if len(ship) == 1]) == 4,
            len([ship for ship in self.ships if len(ship) == 2]) == 3,
            len([ship for ship in self.ships if len(ship) == 3]) == 2,
            len([ship for ship in self.ships if len(ship) == 4]) == 1
        ]
        if not all(conditions):
            raise ValueError("There should be total of 10 ships:\n"
                             "4 single-deck ships;"
                             "3 double-deck ships;"
                             "2 three-deck ships;"
                             "1 four-deck ship.")

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"
        self.field[location].fire(location[0], location[1])
        if self.field[location].is_drowned:
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        field = [["~" for _ in range(10)] for _ in range(10)]
        for location, ship in self.field.items():
            if ship.is_drowned:
                field[location[0]][location[1]] = "x"
            elif ship.get_deck(location[0], location[1]).is_alive:
                field[location[0]][location[1]] = u"\u25A1"
            else:
                field[location[0]][location[1]] = "*"
        for row in field:
            print(row)
