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
            is_drowned : bool = False
    ) -> None:
        if start[0] != end[0]:
            self.decks = [
                Deck(start[0] + i, start[1])
                for i in range(abs(end[0] - start[0]) + 1)
            ]
        elif start[1] != end[1]:
            self.decks = [
                Deck(start[0], start[1] + i)
                for i in range(abs(end[1] - start[1]) + 1)
            ]
        else:
            self.decks = [Deck(start[0], start[1])]

        self.hp = len(self.decks)
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck.is_alive:
            deck.is_alive = False
            self.hp -= 1
        if self.hp == 0:
            self.is_drowned = True
            return "Sunk!"
        return "Hit!"


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field, self.ships = {}, {}
        for ship in ships:
            ship_reference = Ship(ship[0], ship[1])
            ship_len = len(ship_reference.decks)
            self.ships[ship_len] = self.ships.get(ship_len, 0) + 1
            for deck in ship_reference.decks:
                self.field[(deck.row, deck.column)] = ship_reference
        self._validate_field()

    def fire(self, location: tuple) -> str:
        if location in self.field:
            return self.field[location].fire(location[0], location[1])
        return "Miss!"

    def print_field(self) -> None:
        field = ""
        for row in range(10):
            for column in range(10):
                if (row, column) in self.field:
                    ship = self.field[(row, column)]
                    if ship.is_drowned:
                        field += "x"
                    elif ship.get_deck(row, column).is_alive:
                        field += u"\u25A1"
                    else:
                        field += "*"
                else:
                    field += "~"
            field += "\n"

        print(field)

    def _validate_field(self) -> None:
        expected = {4: 1, 3: 2, 2: 3, 1: 4}
        if self.ships != expected:
            raise ValueError("Invalid ships count")

        for (row, column), ship in self.field.items():
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    if dr == 0 and dc == 0:
                        continue
                    neighbor_r, neighbor_c = row + dr, column + dc
                    if (0 <= neighbor_r <= 9 and 0 <= neighbor_c <= 9
                            and (neighbor_r, neighbor_c) in self.field
                            and self.field[(neighbor_r, neighbor_c)]
                            is not ship):
                        raise ValueError(
                            f"Ships touch at ({neighbor_r}, {neighbor_c})"
                        )
