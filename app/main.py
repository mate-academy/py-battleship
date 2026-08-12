class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
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
        self.is_drowned = is_drowned
        self.decks = []

        if start[0] == end[0]:
            row = start[0]
            for col in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
                self.decks.append(Deck(row, col))
        else:
            col = start[1]
            for row in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
                self.decks.append(Deck(row, col))

    def get_deck(self, row: int, column: int) -> "Deck":
        for deck_item in self.decks:
            if deck_item.row == row and deck_item.column == column:
                return deck_item

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        deck.is_alive = False

        self.is_drowned = True
        for deck_item in self.decks:
            if deck_item.is_alive:
                self.is_drowned = False
                break


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        for coordinates in ships:
            ship = Ship(coordinates[0], coordinates[1])
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

        self._validate_field()

    def _validate_field(self) -> None:
        unique_ships = list(set(self.field.values()))

        if len(unique_ships) != 10:
            raise ValueError("Invalid number of ships")

        lengths = [len(ship.decks) for ship in unique_ships]

        if (
                lengths.count(1) != 4
                or lengths.count(2) != 3
                or lengths.count(3) != 2
                or lengths.count(4) != 1
        ):
            raise ValueError("Invalid ship sizes")

        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for (row, col), ship in self.field.items():
            for dr, dc in directions:
                neighbor = (row + dr, col + dc)

                if neighbor in self.field and self.field[neighbor] != ship:
                    raise ValueError("Ships are touching")

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
        else:
            return "Miss!"

        ship.fire(location[0], location[1])

        if ship.is_drowned:
            return "Sunk!"
        else:
            return "Hit!"

    def print_field(self) -> None:
        for row in range(10):
            for col in range(10):
                if (row, col) not in self.field:
                    print("~", end="\t")
                else:
                    ship = self.field[(row, col)]
                    deck = ship.get_deck(row, col)

                    if ship.is_drowned:
                        print("x", end="\t")
                    elif deck.is_alive:
                        print(u"\u25A1", end="\t")
                    else:
                        print("*", end="\t")
            print()
