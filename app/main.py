class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive
        self.image: str = f"'{u"\u25A1"}'"

    def __repr__(self) -> str:
        return self.image


class Ship:
    def __init__(
            self,
            start: tuple[int],
            end: tuple[int],
            is_drowned: bool = False
    ) -> None:
        self.decks = []
        if start[0] == end[0]:
            for i in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], i))
        else:
            for i in range(start[0], end[0] + 1):
                self.decks.append(Deck(i, end[1]))

        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if (deck.row, deck.column) == (row, column):
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
        self.is_drowned = all(not deck.is_alive for deck in self.decks)


class Battleship:
    def __init__(self, ships: list[tuple[int]]) -> None:
        self.field = {}
        for ship in ships:
            ship = Ship(ship[0], ship[1])
            coordinates = []
            for deck in ship.decks:
                coordinates.append((deck.row, deck.column))
            self.field[*coordinates] = ship

    def fire(self, location: tuple[int]) -> str:
        for coordinates, ship in self.field.items():
            if location in coordinates:
                ship.fire(*location)
                if not ship.is_drowned:

                    for deck in ship.decks:
                        if (deck.row, deck.column) == location:
                            deck.image = "'*'"
                    return "Hit!"

                for deck in ship.decks:
                    deck.image = "'x'"
                return "Sunk!"
        return "Miss!"

    def print_field(self) -> None:
        field = [["~" for _ in range(10)] for _ in range(10)]

        for ship in self.field.values():
            for deck in ship.decks:
                field[deck.row][deck.column] = deck

        for row in field:
            print(row)
