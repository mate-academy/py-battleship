from typing import Union


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple, end: tuple, is_drowned: bool = False
                 ) -> None:
        self.decks = (
            [
                Deck(x, y)
                for x in range(start[0], end[0] + 1)
                for y in range(start[1], end[1] + 1)
            ])
        self.is_drowned = is_drowned

    def fire(self, row: int, column: int) -> Union[str, None]:
        result_get_deck = self.get_deck(row, column)
        if result_get_deck is not None:
            result_get_deck.is_alive = False
            self.is_drowned = not any([deck.is_alive for deck in self.decks])
            if self.is_drowned:
                return "Sunk!"
            return "Hit!"

    def get_deck(self, row: int, column: int) -> Union[Deck, None]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = [Ship(*ship) for ship in ships]

    def fire(self, location: tuple) -> str:
        for ship in self.ships:
            if ship.fire(*location) is not None:
                return ship.fire(*location)
        return "Miss!"

    def __repr__(self) -> str:
        matrix = [["~" for _ in range(10)]for _ in range(10)]
        for ship in self.ships:
            for deck in ship.decks:
                matrix[deck.row][deck.column] = ("□"
                                                 if deck.is_alive is True
                                                 else "*")
        return "".join(["  ".join(row) + "\n" for row in matrix])

    def _validate_field(self) -> bool:
        real = {4: 0, 3: 0, 2: 0, 1: 0}
        must_be = {4: 1, 3: 2, 2: 3, 1: 4}
        if len(self.ships) != 10:
            return False
        for ship in self.ships:
            print(len(ship.decks))
            real[len(ship.decks)] += 1
        return real == must_be
