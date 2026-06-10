class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple
    ) -> None:
        self.is_drowned = False
        self.decks = []
        if start[0] == end[0]:
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], column))
        else:
            for row in range(start[0], end[0] + 1):
                self.decks.append(Deck(row, start[1]))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        self.is_drowned = all(not deck.is_alive for deck in self.decks)


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        for ship in ships:
            the_ship = Ship(ship[0], ship[1])
            for deck in the_ship.decks:
                self.field[(deck.row, deck.column)] = the_ship
        self._validate_field()

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            ship.fire(location[0], location[1])
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                if (row, column) not in self.field:
                    print("~", end=" ")
                else:
                    ship = self.field[(row, column)]
                    deck = ship.get_deck(row, column)
                    if ship.is_drowned:
                        print("x", end=" ")
                    elif not deck.is_alive:
                        print("*", end=" ")
                    else:
                        print(u"\u25A1", end=" ")
            print()

    def _validate_field(self) -> None:
        ships = set(self.field.values())
        one_deck = [ship for ship in ships if len(ship.decks) == 1]
        two_deck = [ship for ship in ships if len(ship.decks) == 2]
        three_deck = [ship for ship in ships if len(ship.decks) == 3]
        four_deck = [ship for ship in ships if len(ship.decks) == 4]

        if len(ships) != 10:
            raise ValueError("the total number of the ships should be 10")
        if len(one_deck) != 4:
            raise ValueError("there should be 4 single-deck ships")
        if len(two_deck) != 3:
            raise ValueError("there should be 3 double-deck ships")
        if len(three_deck) != 2:
            raise ValueError("there should be 2 three-deck ships")
        if len(four_deck) != 1:
            raise ValueError("there should be 1 four-deck ship")

        for ship in ships:
            for deck in ship.decks:
                for row_difference in range(-1, 2):
                    for column_difference in range(-1, 2):
                        neighbor = (
                            deck.row + row_difference,
                            deck.column + column_difference
                        )
                        if (
                                neighbor in self.field
                                and self.field[neighbor] is not ship
                        ):
                            raise ValueError(
                                "ships shouldn't be located"
                                " in the neighboring cells"
                            )
