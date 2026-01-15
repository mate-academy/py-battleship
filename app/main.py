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
        self.decks = [
            Deck(row, column)
            for row in range(start[0], end[0] + 1)
            for column in range(start[1], end[1] + 1)
        ]
        self.alive_decks = len(self.decks)
        self.start = start
        self.end = end

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        self.alive_decks -= 1
        if self.alive_decks == 0:
            self.is_drowned = True

    def __repr__(self) -> str:
        return f"Ship {self.start} - {self.end}"


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = [Ship(*ship) for ship in ships]
        self.field = {}
        for ship in self.ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship
        self.field_image = self._draw_field()
        self._validate_field()

    def fire(self, coordinates: tuple) -> str:
        if coordinates not in self.field:
            return "Miss!"

        ship = self.field.get(coordinates)
        ship.fire(*coordinates)
        deck = ship.get_deck(*coordinates)
        deck.is_alive = False

        if not ship.is_drowned:
            self.field_image[deck.row][deck.column] = "*"
            return "Hit!"

        for deck in ship.decks:
            self.field_image[deck.row][deck.column] = "x"
        return "Sunk!"

    def _draw_field(self) -> list:
        field = []
        for row in range(10):
            field.append([])
            for column in range(10):
                if self.field.get((row, column)):
                    field[-1].append("\u25A1")
                else:
                    field[-1].append(".")
        return field

    def print_field(self) -> None:
        print("\t", "\t".join([str(num) for num in range(10)]))
        for column, row in enumerate(self.field_image):
            print(column, "\t", "\t".join(row))

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError(f"The total number of the ships should be `10`."
                             f"Actual amount is `{len(self.ships)}`.")

        ships_number = dict.fromkeys(list(range(1, 5)), 0)
        for ship in self.ships:
            ships_number[len(ship.decks)] += 1
        for ship_length, number in ships_number.items():
            if 5 - ship_length != number:
                raise ValueError(f"The amount of {ship_length}-deck ships "
                                 f"should be `{5 - ship_length}`. "
                                 f"Actual amount is `{number}`.")

        for ship in self.ships:
            neighbour_cells = self._get_neighbours(ship.start, ship.end)
            for cell in neighbour_cells:
                if cell in self.field:
                    raise ValueError(f"{ship} should be moved. Ships shouldn't"
                                     f" be located in the neighboring cells.")

    @staticmethod
    def _get_neighbours(start: tuple, end: tuple) -> list[tuple]:
        neighbour_cells = [
            (start[0] - 1, start[1] - 1),
            (start[0] - 1, end[1] + 1),
            (end[0] + 1, start[1] - 1),
            (end[0] + 1, end[1] + 1)
        ]

        def add_side(
                start: tuple,
                end: tuple,
                neighbour_cells: list[tuple]
        ) -> list[tuple]:

            side = []
            for row in range(start[0], end[0] + 1):
                for column in range(start[1], end[1] + 1):
                    side.append((row, column))
            return neighbour_cells + side

        sides_ends = [
            ((start[0] - 1, start[1]), (start[0] - 1, end[1])),
            ((end[0] + 1, start[1]), (end[0] + 1, end[1])),
            ((start[0], start[1] - 1), (end[0], start[1] - 1)),
            ((start[0], end[1] + 1), (end[0], end[1] + 1))
        ]

        for start, end in sides_ends:
            neighbour_cells = add_side(start, end, neighbour_cells)

        existing_neighbour_cells = []
        for coordinates in neighbour_cells:
            if 0 <= coordinates[0] <= 9 and 0 <= coordinates[1] <= 9:
                existing_neighbour_cells.append(coordinates)

        return existing_neighbour_cells
