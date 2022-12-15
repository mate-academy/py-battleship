class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
        self, start: tuple, end: tuple, is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned
        self.decks = []
        for row in range(start[0], end[0] + 1):
            for col in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, col))

    def get_deck(self, row: int, column: int) -> Deck:
        return list(
            filter(
                lambda deck: (deck.row, deck.column) == (row, column),
                self.decks,
            )
        )[0]

    def fire(self, row: int, column: int) -> None:
        for deck in self.decks:
            if (deck.row, deck.column) == (row, column):
                deck.is_alive = False

        if not any([deck.is_alive for deck in self.decks]):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        for ship_tuple in ships:
            ship = Ship(ship_tuple[0], ship_tuple[1])
            for deck in ship.decks:
                self.field[deck.row, deck.column] = ship

    def fire(self, location: tuple) -> str:
        if location in self.field:
            self.field[location].fire(location[0], location[1])
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(11):
            for col in range(11):
                if (row, col) in self.field:
                    if self.field[row, col].is_drowned:
                        print("x  ", end="")
                    elif self.field[row, col].get_deck(row, col).is_alive:
                        print("\u25A1  ", end="")
                    else:
                        print("*  ", end="")
                else:
                    print("~  ", end="")
            print("")


ships = [
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
#
# battle_ship = Battleship(ships)
# battle_ship.print_field()
#
# print(
#     battle_ship.fire((0, 4)),  # Miss!
#     battle_ship.fire((0, 3)),  # Hit!
#     battle_ship.fire((0, 2)),  # Hit!
#     battle_ship.fire((0, 1)),  # Hit!
#     battle_ship.fire((0, 0)),  # Sunk!
#     battle_ship.fire((0, 5)),  # !
#     battle_ship.fire((0, 5)),  # !
# )
# battle_ship.print_field()
