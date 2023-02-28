from typing import Optional


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
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.decks = []
        row1, col1 = start
        row2, col2 = end
        for row in range(row1, row2 + 1):
            for col in range(col1, col2 + 1):
                self.decks.append(Deck(row, col))
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck is not None:
            deck.is_alive = False
            self.is_drowned = all(
                not deck.is_alive for deck in self.decks
            )


class Battleship:
    def __init__(self, ships: list[Ship]) -> None:
        self.field = {}
        for ship in ships:
            ship_obj = Ship(ship[0], ship[1])
            for deck in ship_obj.decks:
                self.field[(deck.row, deck.column)] = ship_obj
        self._validate_field()

    def print_field(self) -> None:
        field = [["~" for _ in range(10)] for _ in range(10)]
        for ship in set(self.field.values()):
            for deck in ship.decks:
                if ship.is_drowned:
                    field[deck.row][deck.column] = "x"
                elif deck.is_alive:
                    field[deck.row][deck.column] = "\u25A1"
                else:
                    field[deck.row][deck.column] = "*"
        for row in field:
            print(*row)

    def _validate_field(self) -> None:
        decks_number = [len(deck.__dict__["decks"])
                        for deck in set(self.field.values())]

        if len(decks_number) != 10:
            raise Exception("The total number of the ships should be 10")

        if decks_number.count(1) != 4:
            raise Exception("There should be 4 single-deck ships")

        if decks_number.count(2) != 3:
            raise Exception("There should be 3 double-deck ships")

        if decks_number.count(3) != 2:
            raise Exception("There should be 2 three-deck ships")

        if decks_number.count(4) != 1:
            raise Exception("There should be 1 four-deck ship")

        for coords, ship in self.field.items():
            for row in range(coords[0] - 1, coords[0] + 2):
                for column in range(coords[1] - 1, coords[1] + 2):
                    if (
                        (row, column) in self.field
                        and self.field[(row, column)] != ship
                    ):
                        raise Exception(
                            "Ships cannot be located in neighboring cells"
                        )

    def fire(self, location: tuple[int, int]) -> str:
        if location in self.field.keys():
            self.field[location].fire(location[0], location[1])
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"
