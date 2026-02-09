from typing import Tuple, Generator, Any, List


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: Tuple[int, int],
            end: Tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.decks = [
            Deck(row, col)
            for row, col in self._generate_decks(start, end)
        ]
        self.is_drowned = is_drowned

    @staticmethod
    def _generate_decks(
            start: Tuple[int, int],
            end: Tuple[int, int]
    ) -> Generator[tuple[int, int], Any, None]:
        start_row, start_column = start
        end_row, end_column = end

        if start_row == end_row:
            return (
                (start_row, col)
                for col in range(start_column, end_column + 1)
            )
        elif start_column == end_column:
            return (
                (row, start_column)
                for row in range(start_row, end_row + 1)
            )

    def fire(self, row: int, column: int) -> str:
        deck = next(
            (deck for deck in self.decks
             if deck.row == row and deck.column == column),
            None,
        )
        if deck:
            deck.is_alive = False
            self.update_drowned_status()
            return "Hit!" if not self.is_drowned else "Sunk!"
        else:
            return "Miss!"

    def update_drowned_status(self) -> None:
        self.is_drowned = not any(deck.is_alive for deck in self.decks)


class Battleship:
    def __init__(
            self,
            ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        self.field: dict[Tuple[int, int], Ship] = {}
        for ship_start, ship_end in ships:
            ship = Ship(ship_start, ship_end)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: Tuple[int, int]) -> str:
        ship = self.field.get(location)
        if ship is not None:
            return ship.fire(*location)
        else:
            return "Miss!"
