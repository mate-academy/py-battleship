from typing import Any


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False
                 ) -> None:

        self.start = start
        self.end = end
        self.is_drowned = is_drowned

        self.decks = [
            Deck(row, column)
            for row in range(start[0], end[0] + 1)
            for column in range(start[1], end[1] + 1)
        ]

    def get_deck(self, row: int, column: int) -> Deck | Any | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck.is_alive:
            deck.is_alive = False
            if all(not check_deck.is_alive for check_deck in self.decks):
                self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = [Ship(ship[0], ship[1]) for ship in ships]

        self.field = {
            (deck.row, deck.column): ship
            for ship in self.ships
            for deck in ship.decks
        }

        self.show_field = [
            [u"\u25A1" if (row, column) in self.field else "~"
             for column in range(10)] for row in range(10)
        ]
        self._validate_field()

    def _validate_field(self) -> None:

        all_ships = len(self.ships)

        single_deck_ships = sum(
            1 for ship in self.ships if len(ship.decks) == 1)

        double_deck_ships = sum(
            1 for ship in self.ships if len(ship.decks) == 2)

        three_deck_ships = sum(
            1 for ship in self.ships if len(ship.decks) == 3)

        four_deck_ships = sum(
            1 for ship in self.ships if len(ship.decks) == 4)

        if (
                all_ships != 10
                or single_deck_ships != 4
                or double_deck_ships != 3
                or three_deck_ships != 2
                or four_deck_ships != 1
        ):
            raise ValueError("Incorrect configurations of ships")

        for check_ship1 in self.ships:
            for check_ship2 in self.ships:
                if check_ship1 != check_ship2:
                    for check_deck1 in check_ship1.decks:
                        for check_deck2 in check_ship2.decks:

                            if (abs(check_deck1.row
                                    - check_deck2.row) <= 1
                                    and abs(check_deck1.column
                                            - check_deck2.column) <= 1):
                                raise ValueError(
                                    "Ships are located in neighboring cells")

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            ship.fire(*location)
            if ship.is_drowned:

                for coordinate, is_ship in self.field.items():
                    if is_ship == ship:
                        row, col = coordinate
                        self.show_field[row][col] = "X"
                return "Sunk!"

            self.show_field[location[0]][location[1]] = "*"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        print("")
        for row in self.show_field:
            print(row)


if __name__ == "__main__":
    battle_ship = Battleship(
        ships=[
            ((0, 0), (0, 3)),
            ((0, 5), (0, 6)),
            ((0, 8), (0, 9)),
            ((2, 0), (4, 0)),
            ((2, 4), (2, 6)),
            ((2, 8), (2, 9)),
            ((9, 9), (9, 9)),
            ((7, 7), (7, 7)),
            ((7, 9), (7, 9)),
            ((9, 7), (9, 7)),

        ]
    )

    results = [
        battle_ship.fire((9, 7)),
        battle_ship.fire((0, 0)),
        battle_ship.fire((0, 4)),
        battle_ship.fire((0, 1)),
        battle_ship.fire((0, 2)),
        battle_ship.fire((0, 3)),
        battle_ship.fire((9, 3)),
        battle_ship.fire((2, 8)),
        battle_ship.fire((0, 5)),
    ]

    print(results)
    battle_ship.print_field()
