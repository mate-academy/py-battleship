class Deck:
    def __init__(
            self,
            row: int,
            column: int,
            is_alive: bool = True
    ) -> None:
        self.location = (row, column)
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        if start[0] == end[0]:
            self.decks = [
                Deck(start[0], column)
                for column in range(start[1], end[1] + 1)
            ]
        else:
            self.decks = [
                Deck(row, start[1])
                for row in range(start[0], end[0] + 1)
            ]
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.location == (row, column):
                return deck

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False

        if all(deck.is_alive is False for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        self.field = {}
        for start, end in ships:
            ship = Ship(start, end)
            for deck in ship.decks:
                self.field[deck.location] = ship

        self._validate_field()

    def _validate_field(self) -> None:
        ships = set(self.field.values())

        if len(ships) != 10:
            raise ValueError("The total number of ships should be 10")

        count_ship_len = {1: 0, 2: 0, 3: 0, 4: 0}
        for ship in ships:
            count_ship_len[len(ship.decks)] += 1

        if count_ship_len != {1: 4, 2: 3, 3: 2, 4: 1}:
            raise ValueError("Invalid number of ships by length")

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
        for ship in ships:
            for deck in ship.decks:
                row, col = deck.location
                for dr, dc in directions:
                    neighbor = (row + dr, col + dc)
                    if neighbor in self.field and self.field[neighbor] != ship:
                        raise ValueError("Ships should not be located "
                                         "in neighboring cells")

    def fire(self, location: tuple[int, int]) -> str:
        if location not in self.field:
            return "Miss!"

        ship = self.field[location]
        ship.fire(*location)

        if ship.is_drowned:
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        field = [["~" for _ in range(10)] for _ in range(10)]

        for location, ship in self.field.items():
            row, column = location
            if ship.is_drowned:
                field[row][column] = "x"
            elif not ship.get_deck(row, column).is_alive:
                field[row][column] = "*"
            else:
                field[row][column] = "□"

        for row in field:
            print(" ".join(row))
