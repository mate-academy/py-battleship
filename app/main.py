class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive if is_alive in [True, False] else True

    def hit(self) -> None:
        self.is_alive = False


class Ship:
    def __init__(self, start: tuple, end: tuple) -> None:
        self.decks = []
        self.is_drowned = False
        self._create_decks(start, end)

    def _create_decks(self, start: tuple, end: tuple) -> None:
        if start[0] == end[0]:
            for col in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], col))
        elif start[1] == end[1]:
            for row in range(start[0], end[0] + 1):
                self.decks.append(Deck(row, start[1]))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> Deck | None:
        deck = self.get_deck(row, column)
        if deck:
            deck.hit()
            self.is_drowned = all(not d.is_alive for d in self.decks)
            if self.is_drowned not in [True, False]:
                self.is_drowned = False
            return deck
        return None


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        self._initialize_field(ships)

    def _initialize_field(self, ships: list) -> None:
        for start, end in ships:
            ship = Ship(start, end)
            for deck in ship.decks:
                if (deck.row, deck.column) in self.field:
                    raise ValueError(f"Conflict at position {deck.row}",
                                     f" {deck.column}")
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        ship = self.field.get(location)
        if not ship:
            return "Miss!"

        deck = ship.fire(location[0], location[1])
        if deck:
            return "Sunk!" if ship.is_drowned else "Hit!"
        return "Miss!"
