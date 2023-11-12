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
        self.is_drowned = is_drowned
        self.decks = [
            Deck(row, column)
            for column in range(start[1], end[1] + 1)
            for row in range(start[0], end[0] + 1)
        ]

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        if not any(deck.is_alive for deck in self.decks):
            self.is_drowned = True
            return "Sunk!"
        else:
            return "Hit!"


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = ships

        self.ships = [
            Ship(coord[0], coord[-1])
            for coord in ships
        ]
        self.field = {
            (deck.row, deck.column): ship
            for ship in self.ships
            for deck in ship.decks
        }

    def _validate_field(self) -> None:
        fleet = [len(self.ships) == 10]

        for len_ship, quantity in enumerate(range(4, 0, -1)):
            fleet.append(
                sum(ship for ship in self.ships
                    if len(ship) == (len_ship + 1) == quantity)
            )
        if not all(fleet):
            raise ValueError("The fleet does not meet the conditions.")

    def __str__(self) -> str:
        field = [["*" for _ in range(10)] for _ in range(10)]
        for ceil in self.field.keys():
            ship = self.field[ceil]
            if ship.is_drowned:
                field[ceil[0]][ceil[1]] = "X"
            else:
                field[ceil[0]][ceil[1]] = str(ship.get_deck(ceil[0], ceil[1]))
        return "\n".join(["   ".join(row) for row in field])

    def fire(self, location: tuple) -> str:
        loc_x, loc_y = location
        if location in self.field.keys():
            return self.field[location].fire(loc_x, loc_y)
        else:
            return "Miss!"
