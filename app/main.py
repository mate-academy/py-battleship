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
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        r1, r2 = sorted((start[0], end[0]))
        c1, c2 = sorted((start[1], end[1]))

        if r1 == r2:
            self.decks = [Deck(r1, c) for c in range(c1, c2 + 1)]
        else:
            self.decks = [Deck(r, c1) for r in range(r1, r2 + 1)]

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if all(not deck.is_alive for deck in self.decks):
                self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        for start, end in ships:
            current_ship = Ship(start, end)
            for deck in current_ship.decks:
                self.field[(deck.row, deck.column)] = current_ship
        self._validate_field(ships)

    def fire(self, location: tuple) -> str:
        if location in self.field:
            target_ship = self.field[location]
            target_ship.fire(location[0], location[1])
            if target_ship.is_drowned:
                return "Sunk!"
            else:
                return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                ship = self.field.get((row, column))
                if not ship:
                    print("~", end=" ")
                    continue
                deck = ship.get_deck(row, column)
                if ship.is_drowned:
                    print("x", end=" ")
                elif deck.is_alive:
                    print(u"\u25A1", end=" ")
                else:
                    print("*", end=" ")
            print()

    def _validate_field(self, ships_coordinates: list[tuple]) -> None:
        lengths = []
        for start, end in ships_coordinates:
            length = abs(start[0] - end[0]) + abs(start[1] - end[1]) + 1
            lengths.append(length)

        if len(lengths) != 10:
            raise ValueError

        expected = {1: 4, 2: 3, 3: 2, 4: 1}

        for size, count in expected.items():
            if lengths.count(size) != count:
                raise ValueError("The number of ships is incorrect")

        for (row, column), current_ship in self.field.items():
            for delta_row in range(-1, 2):
                for delta_column in range(-1, 2):
                    neighbor_r, neighbor_c = (
                        row + delta_row, column + delta_column
                    )
                    if 0 <= neighbor_r < 10 and 0 <= neighbor_c < 10:
                        neighbor_ship = (
                            self.field.get((neighbor_r, neighbor_c))
                        )
                        if (
                                neighbor_ship is not None
                                and neighbor_ship is not current_ship
                        ):
                            raise ValueError("The ships are touching")
        return True
