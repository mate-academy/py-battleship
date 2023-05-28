from typing import List, Optional


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return f"Deck: {self.row}, {self.column}, {self.is_alive}"


class Ship:
    def __init__(self, start: int, end: int, is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = [
            Deck(row=row, column=column)
            for row in range(self.start[0], self.end[0] + 1)
            for column in range(self.start[1], self.end[1] + 1)
        ]

    def __repr__(self) -> str:
        return f"Ship: {self.start}, {self.end}, {self.is_drowned}"

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        return next(
            (
                deck for deck in self.decks
                if row == deck.row and column == deck.column
            ),
            None
        )

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        sunk_check_list = [deck.is_alive for deck in self.decks]
        if any(sunk_check_list):
            return "Hit!"
        self.is_drowned = True
        return "Sunk!"


class Battleship:
    def __init__(self, ships: List[tuple]) -> None:
        self.ships = [
            Ship(start=ship[0], end=ship[1]) for ship in ships
        ]
        self.all_ship_decks = {
            ship.decks[i]: ship for ship in self.ships
            for i in range(len(ship.decks))
        }
        self._validate_field()

    def _validate_field(self) -> None:
        decks_number = [len(ship.decks) for ship in self.ships]

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

        for deck, ship in self.all_ship_decks.items():
            for row in range(deck.row - 1, deck.row + 2):
                for column in range(deck.column - 1, deck.column + 2):
                    if (
                            (row, column) in
                            [(deck.row, deck.column)
                             for deck in self.all_ship_decks.keys()]
                            and next(
                                self.all_ship_decks[deck]
                                for deck in self.all_ship_decks
                                if (row, column) == (deck.row, deck.column)
                            ) != ship
                    ):
                        raise Exception(
                            "Ships cannot be located in neighboring cells"
                        )

    def fire(self, cell: tuple) -> str:
        if cell not in [
            (deck.row, deck.column) for deck in self.all_ship_decks.keys()
        ]:
            return "Miss!"
        ship = next(
            self.all_ship_decks[deck] for deck in self.all_ship_decks
            if cell == (deck.row, deck.column)
        )
        return ship.fire(*cell)

    def print_field(self) -> None:
        field_list = [["~" for _ in range(10)] for _ in range(10)]
        for ship in self.all_ship_decks.values():
            if ship.is_drowned:
                for deck in ship.decks:
                    field_list[deck.row][deck.column] = "x"
            else:
                for deck in ship.decks:
                    if not deck.is_alive:
                        field_list[deck.row][deck.column] = "*"
                    else:
                        field_list[deck.row][deck.column] = "□"
        for row in field_list:
            print(*row)
