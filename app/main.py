from __future__ import annotations


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __eq__(self, other: Deck) -> bool:
        return self.row == other.row and self.column == other.column

    def tuple(self) -> tuple[int, int]:
        return self.row, self.column


class Ship:
    def __init__(self,
                 start: tuple[int, int],
                 end: tuple[int, int],
                 is_drowned: bool = False) -> None:
        self.decks = Ship._create_decks(start, end)
        self.is_drowned = is_drowned
        self.length = len(self.decks)

    def get_deck(self, row: int, column: int) -> Deck:
        return self.decks[self.decks.index(Deck(row, column))]

    def fire(self, row: int, column: int) -> str:
        self.get_deck(row, column).is_alive = False
        if [deck.is_alive for deck in self.decks].count(True) == 0:
            self.is_drowned = True
            return "Sunk!"
        return "Hit!"

    @staticmethod
    def _create_decks(start: tuple[int, int],
                      end: tuple[int, int]) -> list[Deck]:
        return [Deck(row, column) for row in range(start[0], end[0] + 1)
                for column in range(start[1], end[1] + 1)]


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = dict()
        ships = [Ship(start, end) for start, end in ships]
        for ship in ships:
            for deck in ship.decks:
                self.field[deck.tuple()] = ship

    def fire(self, location: tuple) -> str:
        if location in self.field:
            return self.field[location].fire(*location)
        return "Miss!"

    def print_filed(self) -> None:
        for row in range(10):
            game_row = ""
            for column in range(10):
                cell = (row, column)
                if cell in self.field:
                    if self.field[cell].is_drowned:
                        game_row += "X\t"
                    elif self.field[cell].get_deck(row, column).is_alive:
                        game_row += "O\t"
                    else:
                        game_row += "*\t"
                game_row += "~\t"
            print(game_row)

    def _validate_field(self) -> bool:
        ship_lengths = [ship.length for ship in set(self.field.values())]

        if len(ship_lengths) != 10:
            return False

        if ship_lengths.count(4) != 1:
            return False
        if ship_lengths.count(3) != 2:
            return False
        if ship_lengths.count(2) != 3:
            return False
        if ship_lengths.count(1) != 4:
            return False

        for cell, ship in self.field.items():
            for neighbour in self._get_neighbours(cell):
                if neighbour in self.field and self.field[neighbour] != ship:
                    return False

        return True

    @staticmethod
    def _get_neighbours(cell: tuple[int, int]) -> list[tuple[int, int]]:
        row, column = cell
        return [
            (row - 1, column),
            (row - 1, column + 1),
            (row, column + 1),
            (row + 1, column + 1),
            (row + 1, column),
            (row + 1, column - 1),
            (row, column - 1),
            (row - 1, column - 1),
        ]
