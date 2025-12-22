from app.battleship_error import (
    TotalShipsAmountError,
    DeckAmountError,
    LocationError
)


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return f"[{self.row}, {self.column}, is_alive: {self.is_alive}]"


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: int = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned

        self.decks = []
        self._create_decks()

    def __repr__(self) -> str:
        return f"[{self.start}, {self.end}, is_drowned: {self.is_drowned}]"

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False

        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True

    def _create_decks(self) -> None:
        size_x = self.end[0] - self.start[0]
        size_y = self.end[1] - self.start[1]
        self.size = size_x + 1 if size_x >= size_y else size_y + 1

        for i in range(self.size):
            self.decks.append(Deck(
                row=self.start[0] + i if size_x else self.start[0],
                column=self.start[1] if size_x else self.start[1] + i
            ))


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = []
        self._create_ships(ships)

        self.field = self._create_field()

        self._validate_field()

    def fire(self, location: tuple) -> str:
        if location in self.field:
            self.field[location].fire(*location)
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for column in range(10):
            for row in range(10):
                location = column, row
                if location in self.field:
                    if self.field[location].is_drowned:
                        print("x\t", end="")
                    elif not self.field[location].get_deck(location).is_alive:
                        print("*\t", end="")
                    else:
                        print(u"\u25A1\t", end="")
                else:
                    print("~\t", end="")
            print("\n")

    def _create_ships(self, ships: list[tuple]) -> None:
        for ship in ships:
            self.ships.append(Ship(
                start=ship[0],
                end=ship[1]
            ))

    def _create_field(self) -> dict:
        return {
            (deck.row, deck.column): ship
            for ship in self.ships
            for deck in ship.decks
        }

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise TotalShipsAmountError

        sizes = [ship.size for ship in self.ships]
        for size in range(1, 5):
            amount_to_be = 5 - size
            actual_amount = sizes.count(size)
            if actual_amount != amount_to_be:
                raise DeckAmountError(amount_to_be, size, actual_amount)

        directions = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
            (1, 1),
            (-1, -1),
            (1, -1),
            (-1, 1)
        ]
        for cell in self.field:
            for direction in directions:
                neighbour_cell = cell[0] + direction[0], cell[1] + direction[1]
                if (
                    neighbour_cell in self.field
                    and self.field[cell] != self.field[neighbour_cell]
                ):
                    raise LocationError
