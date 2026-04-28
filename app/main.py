class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return f"Deck({self.row}, {self.column}, {self.is_alive})"


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
        self.decks = None
        self.initialize_decks()

    def initialize_decks(self) -> None:
        self.decks = {}
        if self.start == self.end:
            self.decks[self.start] = Deck(
                row=self.start[0], column=self.start[1]
            )

        elif self.start[0] == self.end[0]:
            start_col = min(self.start[1], self.end[1])
            end_col = max(self.start[1], self.end[1])
            for current_el in range(start_col, end_col + 1):
                self.decks[(self.start[0], current_el)] = Deck(
                    row=self.start[0], column=current_el
                )

        elif self.start[1] == self.end[1]:
            start_row = min(self.start[0], self.end[0])
            end_row = max(self.start[0], self.end[0])
            for current_el in range(start_row, end_row + 1):
                self.decks[(current_el, self.end[0])] = Deck(
                    row=current_el, column=self.end[0]
                )

    def get_deck(self, row: int, column: int) -> Deck:
        return self.decks[(row, column)]

    def fire(self, row: int, column: int) -> None:
        fired_deck = self.get_deck(row, column)
        fired_deck.is_alive = False
        if self.check_is_drowned():
            self.is_drowned = True

    def check_is_drowned(self) -> bool:
        return not any(deck.is_alive for deck in self.decks.values())

    def __repr__(self) -> str:
        return f"Ship({self.start}, {self.end}, {self.is_drowned})"


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = [(Ship(start=ship[0], end=ship[1])) for ship in ships]
        self.field = {}
        self.initialize_field()

    def initialize_field(self) -> None:
        for ship in self.ships:
            for r_ship_deck, c_ship_deck in ship.decks.keys():
                self.field[(r_ship_deck, c_ship_deck)] = ship

    def fire(self, location: tuple) -> str:
        row, column = location
        if (row, column) in self.field:
            ship = self.field[row, column]
            ship.fire(row, column)
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        field_visualised = []
        for row in range(10):
            for column in range(10):
                ship = self.field.get((row, column))
                if ship:
                    if ship.is_drowned:
                        field_visualised.append("x")
                    elif not ship.get_deck(row, column).is_alive:
                        field_visualised.append("*")
                    else:
                        field_visualised.append(u"\u25A1")
                else:
                    field_visualised.append("~")

        for i in range(0, 100, 10):
            print("   ".join(field_visualised[i:i + 10]))

    def _validate_field(self) -> None:
        ships_count = len(self.ships)
        if ships_count != 10:
            raise ValueError
        expected = {
            "single-deck": 4,
            "double-deck": 3,
            "three-deck": 2,
            "four-deck": 1
        }
        actual = {
            "single-deck": 0,
            "double-deck": 0,
            "three-deck": 0,
            "four-deck": 0
        }

        for ship in self.ships:
            ship_length = len(ship.decks)
            if ship_length == 4:
                actual["four-deck"] += 1
            elif ship_length == 3:
                actual["three-deck"] += 1
            elif ship_length == 2:
                actual["double-deck"] += 1
            elif ship_length == 1:
                actual["single-deck"] += 1
        if expected != actual:
            raise ValueError

        occupied_cells = {}
        for ship_idx, ship in enumerate(self.ships):
            for row, col in ship.decks.keys():
                print(row, col)
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        neighbor = (row + dr, col + dc)
                        if neighbor in occupied_cells:
                            if neighbor == (row, col):
                                continue
                            if occupied_cells[neighbor] != ship_idx:
                                raise ValueError("Ships are touching!")
                occupied_cells[(row, col)] = ship_idx

    def __repr__(self) -> str:
        return f"Battleship({self.ships})"


battle_ship = Battleship(
    ships=[
        ((0, 0), (0, 3)),
        ((2, 0), (2, 2)),
        ((4, 0), (4, 2)),
        ((6, 0), (6, 1)),
        ((8, 0), (8, 1)),
        ((0, 5), (0, 6)),
        ((2, 5), (2, 5)),
        ((4, 5), (4, 5)),
        ((6, 5), (6, 5)),
        ((8, 5), (8, 5)),
    ]
)


print(
    battle_ship.fire((0, 4)),  # Miss!
    battle_ship.fire((0, 3)),  # Hit!
    battle_ship.fire((0, 2)),  # Hit!
    battle_ship.fire((0, 1)),  # Hit!
    battle_ship.fire((0, 0)),  # Sunk!
)
print(battle_ship.print_field())
print(battle_ship._validate_field())
