class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row: int = row
        self.column: int = column
        self.is_alive: bool = is_alive

    def hit(self) -> None:
        self.is_alive = False


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.decks = self._create_decks(start, end)
        self.is_drowned = is_drowned
        self._validate_ship(start, end)

    def _create_decks(
            self,
            start: tuple[int, int],
            end: tuple[int, int]
    ) -> list[Deck]:
        decks = []
        if start[0] == end[0]:
            for column in range(start[1], end[1] + 1):
                decks.append(Deck(start[0], column))
        else:
            for row in range(start[0], end[0] + 1):
                decks.append(Deck(row, start[1]))

        return decks

    def _validate_ship(
            self,
            start: tuple[int, int],
            end: tuple[int, int]
    ) -> None:
        if not (start[0] == end[0] or start[1] == end[1]):
            raise (ValueError
                   ("Ship must be placed either horizontally or vertically.")
                   )
        if not self.decks:
            raise ValueError("Invalid ship size.")

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck and deck.is_alive:
            deck.hit()
            self.is_drowned = all(not d.is_alive for d in self.decks)
            return "Sunk!" if self.is_drowned else "Hit!"
        return "Miss!"


class Battleship:
    def __init__(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]) -> None:
        self.field = {}
        self.ships = []
        self._initialize_field(ships)
        self._validate_field()

    def _initialize_field(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]) -> None:
        for start, end in ships:
            ship = Ship(start, end)
            self.ships.append(ship)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple[int, int]) -> str:
        if location in self.field:
            ship = self.field[location]
            result = ship.fire(*location)
            return result
        return "Miss!"

    def _validate_field(self) -> None:
        ship_counts = {1: 0, 2: 0, 3: 0, 4: 0}
        for ship in self.ships:
            ship_length = len(ship.decks)
            if ship_length in ship_counts:
                ship_counts[ship_length] += 1
            else:
                raise ValueError(f"Invalid ship length: {ship_length}")

            for deck in ship.decks:
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        neighbor = (deck.row + dx, deck.column + dy)
                        if (neighbor in self.field
                                and self.field[neighbor] != ship):
                            raise ValueError("Ships must not be adjacent.")

        if ship_counts != {1: 4, 2: 3, 3: 2, 4: 1}:
            raise ValueError("Field must contain 1 four-deck, 2 three-deck, "
                             "3 two-deck, and 4 single-deck ships.")

    def print_field(self) -> None:
        for row in range(10):
            for col in range(10):
                if (row, col) in self.field:
                    ship = self.field[(row, col)]
                    deck = ship.get_deck(row, col)
                    if deck and deck.is_alive:
                        print(u"\u25A1", end=" ")
                    else:
                        print("*", end=" ")
                else:
                    print("~", end=" ")
            print()
        print()
