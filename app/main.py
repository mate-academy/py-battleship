class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def hit(self) -> None:
        self.is_alive = False


class Ship:
    def __init__(self, start: tuple, end: tuple) -> None:
        self.decks = []
        self.is_drowned = False

        if start[0] == end[0]:
            for col in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], col))
        elif start[1] == end[1]:
            for row in range(start[0], end[0] + 1):
                self.decks.append(Deck(row, start[1]))
        else:
            raise ValueError("Ships must be either horizontal or vertical.")

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> bool:
        fired_deck = self.get_deck(row, column)
        if fired_deck:
            fired_deck.hit()
            if all(not deck.is_alive for deck in self.decks):
                self.is_drowned = True
            return True
        return False


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = []
        self.field = {}
        self.occupied_positions = set()

        for start, end in ships:
            ship = Ship(start, end)
            self.ships.append(ship)

            for deck in ship.decks:
                if (deck.row, deck.column) in self.occupied_positions:
                    raise ValueError(f"Ship overlap at "
                                     f"{(deck.row, deck.column)}")

                self.field[(deck.row, deck.column)] = ship
                self.occupied_positions.add((deck.row, deck.column))

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            hit = ship.fire(*location)
            if hit:
                return "Sunk!" if ship.is_drowned else "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            line = ""
            for col in range(10):
                cell = (row, col)
                if cell not in self.field:
                    line += "~ "
                else:
                    ship = self.field[cell]
                    deck = ship.get_deck(row, col)
                    if deck.is_alive:
                        line += "□ "
                    elif ship.is_drowned:
                        line += "x "
                    else:
                        line += "* "
            print(line)
