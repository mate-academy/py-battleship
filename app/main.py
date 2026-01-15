from dataclasses import dataclass


@dataclass
class Deck:
    row: int
    column: int
    is_alive: bool = True


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned
        self.decks: list[Deck] = [Deck(*start)]
        current = start
        while current != end:
            row, column = current
            row += row < end[0]
            column += column < end[1]
            current = row, column
            self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for item in self.decks:
            if item.row == row and item.column == column:
                return item

    def fire(self, row: int, column: int) -> str:
        if deck := self.get_deck(row, column):
            deck.is_alive = False
            if not any(deck.is_alive for deck in self.decks):
                self.is_drowned = True
                return "Sunk!"
            return "Hit!"
        return "Miss!"


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field: dict[tuple, Ship] = {}
        for row in ships:
            ship = Ship(*row)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship
        self._validate_field()

    def print_field(self) -> None:
        to_print = ["Battleship field"]
        for row in range(10):
            row_print = []
            for column in range(10):
                icon = "~"
                if ship := self.field.get((row, column)):
                    if ship.is_drowned:
                        icon = "x"
                    elif not ship.get_deck(row, column).is_alive:
                        icon = "*"
                    else:
                        icon = u"\u25A1"
                row_print.append(icon)
            to_print.append(" ".join(row_print))
        print("\n".join(to_print))

    def fire(self, location: tuple[int, int]) -> str:
        if ship := self.field.get(location):
            return ship.fire(*location)
        return "Miss!"

    def _validate_field(self) -> None:
        self._validate_range()
        self._validate_types_count()
        self._validate_collisions()

    def _validate_range(self) -> None:
        for key in self.field:
            if not (0 <= key[0] < 10 and 0 <= key[1] < 10):
                raise ValueError("Coordinates can't exceed [0, 9] range")

    def _validate_types_count(self) -> None:
        counter = [0] * 4
        for ship in set(self.field.values()):
            length = len(ship.decks)
            if length > 4:
                raise ValueError("Length should not exceed 4")
            counter[length - 1] += 1
        if counter != [4, 3, 2, 1]:
            raise ValueError("Wrong number of ships")

    def _validate_collisions(self) -> None:
        for (row, column), current_ship in self.field.items():
            combinations = [
                (1, 0), (1, 1), (0, 1), (-1, 1),
                (-1, 0), (-1, -1), (0, -1)
            ]
            for _row, _col in combinations:
                current_cord = row + _row, column + _col
                ship = self.field.get(current_cord)
                if ship and ship != current_ship:
                    raise ValueError("Wrong ship placement")
                if ship and abs(_row) == abs(_col):
                    raise ValueError("Ship can't be placed diagonally")
