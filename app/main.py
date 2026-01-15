class Deck:
    def __init__(self,
                 row: int,
                 column: int,
                 is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __str__(self) -> str:
        return f"{self.row} {self.column} {self.is_alive}"


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        self.is_drowned = is_drowned
        self.decks = []

        if start[0] == end[0]:  # Horizontal
            for col in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], col))
        else:  # Vertical
            for row in range(start[0], end[0] + 1):
                self.decks.append(Deck(row, start[1]))

    def get_deck(self, row: int, column: int) -> Deck | None:
        if decks := list(
            filter(lambda deck: (deck.row == row
                                 and deck.column == column),
                   self.decks)
        ):
            return decks[0]

    def fire(self, row: int, column: int) -> None:
        attacked_deck = self.get_deck(row, column)
        if not attacked_deck:
            raise ValueError("Invalid position")
        attacked_deck.is_alive = False
        is_alive = False
        for deck in self.decks:
            if deck.is_alive:
                is_alive = True
        if not is_alive:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: tuple) -> None:
        self.field = {}
        for ind, ship_cords in enumerate(ships):
            ship = Ship(ship_cords[0], ship_cords[1])
            for ship_deck in ship.decks:
                self.field[ship_deck] = ship

    def fire(self, location: tuple) -> str:
        if not len(filtered := list(
            filter(lambda deck: (deck.row == location[0]
                                 and deck.column == location[1]),
                   self.field.keys())
        )):
            return "Miss!"

        attacked_deck = filtered[0]
        if not attacked_deck.is_alive:
            return "Miss!"
        else:
            self.field[attacked_deck].fire(location[0], location[1])
            if self.field[attacked_deck].is_drowned:
                return "Sunk!"
            return "Hit!"

    def print(self) -> None:
        for deck in self.field.keys():
            print(deck)

        for row in range(10):
            for col in range(10):
                is_deck = len(
                    list(
                        filter(lambda deck: (deck.row == row
                                             and deck.column == col),
                               self.field.keys())
                    )
                )
                if is_deck:
                    print("□", end="")
                else:
                    print("~", end="")
                print("\t\t", end="")
            print("")
