class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.coordinate = (row, column)
        self.is_alive = is_alive

    def __hash__(self) -> int:
        return hash(self.coordinate)

    def __eq__(self, other: type) -> bool:
        if isinstance(other, Deck):
            return self.coordinate == other.coordinate
        return False


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.decks = tuple(
            Deck(*deck) for deck in self.get_all_decks(start, end)
        )
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.coordinate == (row, column):
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        coordinate = self.get_deck(row, column)
        if coordinate:
            coordinate.is_alive = False

    @staticmethod
    def get_all_decks(start: tuple[int], end: tuple[int]) -> list:
        x1, y1 = start
        x2, y2 = end

        if x1 == x2:
            return [(x1, y) for y in range(min(y1, y2) , max(y1, y2) + 1)]

        if y1 == y2:
            return [(x, y1) for x in range(min(x1, x2), max(x1, x2) + 1)]

    def is_alive_deck(self, row: int, column: int) -> bool:
        return self.get_deck(row, column).is_alive

    def __eq__(self, other: type) -> bool:
        if isinstance(other, Ship):
            return self.decks == other.decks
        return False

    def __hash__(self) -> int:
        return hash(self.decks)


class Battleship:
    NEIGHBOR_OFFSETS = [(-1, -1), (-1, 0), (-1, 1),
                        (0, -1), (0, 0), (0, 1),
                        (1, -1), (1, 0), (1, 1)]

    def __init__(self, ships: list) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        ships = [Ship(*ship) for ship in ships]
        self.field = {}
        for ship in ships:
            for deck in ship.decks:
                self.field[deck.coordinate] = ship
        self._validate_field(ships)

    def _validate_field(self, ships: list[Ship]) -> None:
        count_of_ships = {
            4: 0,
            3: 0,
            2: 0,
            1: 0
        }

        assert len(set(self.field.values())) == 10, ValueError

        for ship in ships:
            count_of_ships[len(ship.decks)] += 1

        assert count_of_ships == {4: 1, 3: 2, 2: 3, 1: 4}

        for cell in self.field:
            x, y = cell
            ship = self.field[cell]
            ship_coordinates = {deck.coordinate for deck in ship.decks}

            assert all(
                (x + dx, y + dy) not in self.field
                or (x + dx, y + dy) in ship_coordinates
                for dx, dy in self.NEIGHBOR_OFFSETS
            )

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if location in self.field:
            ship = self.field[location]
            ship.fire(*location)
            if all([not deck.is_alive for deck in ship.decks]):
                ship.is_drowned = True
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        field = [
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ]

        for deck in self.field:
            if not self.field[deck].is_drowned:
                if self.field[deck].is_alive_deck(*deck):
                    field[deck[0]][deck[1]] = u"\u25A1"
                else:
                    field[deck[0]][deck[1]] = "*"
            else:
                field[deck[0]][deck[1]] = "x"

        for i in range(10):
            print(field[i], "\n")


if __name__ == "__main__":
    battle_ship = Battleship(
        ships=[
            ((0, 0), (0, 3)),
            ((0, 5), (0, 6)),
            ((0, 8), (0, 9)),
            ((2, 0), (4, 0)),
            ((2, 4), (2, 6)),
            ((2, 8), (2, 9)),
            ((9, 9), (9, 9)),
            ((7, 7), (7, 7)),
            ((7, 9), (7, 9)),
            ((9, 7), (9, 7)),
        ]
    )

    print(
        battle_ship.fire((0, 4)),  # Miss!
        battle_ship.fire((0, 3)),  # Hit!
        battle_ship.fire((0, 2)),  # Hit!
        battle_ship.fire((0, 1)),  # Hit!
        battle_ship.fire((0, 0)),  # Sunk!
    )
    battle_ship.print_field()
