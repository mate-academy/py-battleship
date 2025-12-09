class Deck:
    def __init__(
            self,
            row: int,
            column: int,
            is_alive: bool = True
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple[int],
            end: tuple[int],
            is_drowned: bool = False
    ) -> None:
        self.decks = []
        self.is_drowned = is_drowned
        start_row, end_row = start[0], end[0]
        start_column, end_column = start[1], end[1]

        if start_row == end_row:
            for i in range(
                    min(start_column, end_column),
                    max(start_column, end_column) + 1
            ):
                self.decks.append(Deck(start_row, i))
        elif start_column == end_column:
            for i in range(
                    min(start_row, end_row),
                    max(start_row, end_row) + 1
            ):
                self.decks.append(Deck(i, end_column))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                return deck
        raise ValueError("Cannot find exact deck")

    def fire(self, row: int, column: int) -> None:
        current_deck = self.get_deck(row, column)
        current_deck.is_alive = False
        if not any(deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(
            self,
            ships: list[tuple[tuple[int], tuple[int]]]
    ) -> None:
        self.ships = [Ship(ship[0], ship[1]) for ship in ships]
        self.field = {}
        self._validate_field()
        for ship in self.ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError("Should be 10 ships")

        ship_sizes = {}
        for ship in self.ships:
            size = len(ship.decks)
            ship_sizes[size] = ship_sizes.get(size, 0) + 1

        required_sizes = {
            1: 4,
            2: 3,
            3: 2,
            4: 1
        }

        if ship_sizes != required_sizes:
            raise ValueError("Wrong ship configuration")

        directions = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1)
        ]
        for (row, col), ship in self.field.items():
            for dr, dc in directions:
                neighbor_row = row + dr
                neighbor_col = col + dc
                neighbor_pos = (neighbor_row, neighbor_col)

                if (
                    0 <= neighbor_row <= 9
                    and 0 <= neighbor_col <= 9
                    and neighbor_pos in self.field
                    and self.field[neighbor_pos] != ship
                ):
                    raise ValueError("Ships are touching")

    def fire(self, location: tuple) -> str:
        if location in self.field:
            current_ship = self.field[location]
            current_ship.fire(location[0], location[1])
            if current_ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        else:
            return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for col in range(10):
                location = (row, col)
                if location in self.field:
                    current_ship = self.field[location]
                    current_deck = current_ship.get_deck(row, col)
                    if current_deck.is_alive:
                        print(u"\u25A1", end="\t")
                    else:
                        print(
                            "x"
                            if current_ship.is_drowned
                            else "*",
                            end="\t"
                        )
                else:
                    print("~", end="\t")
            print()
