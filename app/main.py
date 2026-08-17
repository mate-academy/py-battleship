from collections import Counter
from itertools import product


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple, end: tuple,
                 is_drowned: bool = False) -> None:
        self.is_drowned = is_drowned
        if start[0] == end[0]:
            self.decks = [Deck(start[0], y_coord) for y_coord
                          in range(start[1], end[1] + 1)]
        else:
            self.decks = [Deck(x_coord, start[1]) for x_coord
                          in range(start[0], end[0] + 1)]

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck and deck.is_alive:
            deck.is_alive = False

            if not any(part.is_alive for part in self.decks):
                self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple[
        tuple[int, int], tuple[int, int]
    ]]) -> None:
        self.fleet = []
        self.field = {}
        for start, end in ships:
            ship = Ship(start, end)
            self.fleet.append(ship)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

        self._validate_field()

    def fire(self, location: tuple[int, int]) -> str:
        if location not in self.field.keys():
            return "Miss!"

        cell = self.field[location]
        cell.fire(location[0], location[1])
        if cell.is_drowned:
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        table = [["~" for _ in range(10)] for _ in range(10)]
        for cell_x, cell_y, ship in self.field.items():
            if ship.is_drowned:
                table[cell_x][cell_y] = "x"
            elif not ship.get_deck(cell_x, cell_y).is_alive:
                table[cell_x][cell_y] = "*"
            else:
                table[cell_x][cell_y] = u"\u25A1"

        for row in table:
            print(f"{'\t'.join(row)}")

    def _validate_field(self) -> None:
        displacements = [coords for coords in product([-1, 0, 1], repeat=2)]
        displacements.remove((0, 0))
        for cell_x, cell_y in self.field:
            for change_x, change_y in displacements:
                deck = (cell_x + change_x,
                        cell_y + change_y)
                if self.field.get(deck) not in (
                    None, self.field[(cell_x, cell_y)]
                ):
                    raise ValueError(
                        f"Cell ({cell_x}, {cell_y}) is adjacent "
                        f"to existed deck {deck}"
                    )

        if len(self.fleet) != 10:
            raise ValueError("Ships count should be 10")

        sizes = Counter([len(ship.decks) for ship in self.fleet])
        ships_count = {1: 4, 2: 3, 3: 2, 4: 1}
        for decks, ships in ships_count.items():
            if sizes[decks] != ships:
                raise ValueError(f"Count of {decks}-deck ships "
                                 f"should be {ships}")
