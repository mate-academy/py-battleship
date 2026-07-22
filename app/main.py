class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
        is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned
        self.decks: list[Deck] = []

        start_row = start[0]
        start_col = start[1]
        end_row = end[0]
        end_col = end[1]

        if start_row == end_row:
            min_col = min(start_col, end_col)
            max_col = max(start_col, end_col)

            for col in range(min_col, max_col + 1):
                self.decks.append(Deck(start_row, col))

        elif start_col == end_col:
            min_row = min(start_row, end_row)
            max_row = max(start_row, end_row)

            for row in range(min_row, max_row + 1):
                self.decks.append(Deck(row, start_col))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        target_deck = self.get_deck(row, column)
        if target_deck:
            target_deck.is_alive = False
        is_ship_dead = True

        for deck in self.decks:
            if deck.is_alive:
                is_ship_dead = False
                break

        self.is_drowned = is_ship_dead


class Battleship:
    def __init__(
        self,
        ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        self.ships = ships
        self.field: dict[tuple[int, int], Ship] = {}

        for start, end in ships:
            ship = Ship(start, end)

            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

        self._validate_field()

    def fire(self, location: tuple[int, int]) -> str:
        if location not in self.field:
            return "Miss!"

        target_ship = self.field[location]
        target_ship.fire(location[0], location[1])

        if target_ship.is_drowned:
            return "Sunk!"

        return "Hit!"

    def print_field(self) -> None:
        for row in range(10):
            for col in range(10):
                current_pos = (row, col)

                if current_pos not in self.field:
                    print("~", end="\t")
                else:
                    ship = self.field[current_pos]
                    deck = ship.get_deck(row, col)

                    if ship.is_drowned:
                        print("x", end="\t")
                    elif deck and not deck.is_alive:
                        print("*", end="\t")
                    else:
                        print(u"\u25A1", end="\t")
            print()

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError

        fleet_counts = {1: 0, 2: 0, 3: 0, 4: 0}
        unique_ships = set(self.field.values())

        for ship in unique_ships:
            ship_size = len(ship.decks)
            if ship_size not in fleet_counts:
                raise ValueError
            fleet_counts[ship_size] += 1

        if fleet_counts != {1: 4, 2: 3, 3: 2, 4: 1}:
            raise ValueError

        for row, col in self.field.keys():
            current_ship = self.field[(row, col)]

            neighbors = [
                (row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                (row, col - 1), (row, col + 1),
                (row + 1, col - 1), (row + 1, col), (row + 1, col + 1),
            ]

            for neighbor in neighbors:
                if (
                        neighbor in self.field
                        and self.field[neighbor] != current_ship
                ):
                    raise ValueError
