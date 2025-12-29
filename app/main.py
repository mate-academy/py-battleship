class Deck:
    def __init__(self, cell: tuple[int, int], is_alive: bool = True) -> None:
        self.cell = cell
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        if start != end:
            self.decks = []
            if start[0] == end[0]:
                for i in range(start[1], end[1] + 1):
                    self.decks.append(Deck((start[0], i)))
            elif start[1] == end[1]:
                for i in range(start[0], end[0] + 1):
                    self.decks.append(Deck((i, start[1])))
            else:
                raise ValueError("Ship must be either horizontal "
                                 "or vertical, not diagonal!")
        else:
            self.decks = [Deck(start)]
        self.is_drowned = is_drowned

    def get_deck(self, cell: tuple[int, int]) -> Deck | None:
        for deck in self.decks:
            if deck.cell == cell:
                return deck
        return None

    def fire(self, cell: tuple[int, int]) -> None:
        if deck := self.get_deck(cell):
            deck.is_alive = False
        if not any([deck.is_alive for deck in self.decks]):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        self.field_symb = [["~" for _ in range(10)] for _ in range(10)]

        for start, end in ships:
            ship = Ship(start, end)
            for deck in ship.decks:
                self.field[deck.cell] = ship
                self.field_symb[deck.cell[0]][deck.cell[1]] = u"\u25A1"

    def print_field(self) -> None:
        for row in self.field_symb:
            print("    ".join(row))

    def fire(self, cell: tuple[int, int]) -> str:
        if cell in self.field:
            ship = self.field[cell]
            ship.fire(cell)
            self.field_symb[cell[0]][cell[1]] = "x"
            return "Sunk!" if ship.is_drowned else "Hit!"
        return "Miss!"
