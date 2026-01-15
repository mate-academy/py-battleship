class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []

        self.__create_ship()

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        deck_to_hit = self.get_deck(row, column)
        if deck_to_hit is not None:
            deck_to_hit.is_alive = False
        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True

    def __create_ship(self) -> None:
        # If start coordinates (beginning of the ship) are equal to
        # end coordinates, create a single-deck ship
        if self.start == self.end:
            self.decks.append(Deck(self.start[0], self.start[1]))

        # If the end column is greater than the start column,
        # then create a horizontal ship
        if self.end[1] > self.start[1]:
            for column in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], column))

        # If the end row is greater than the start row,
        # then create a vertical ship
        if self.end[0] > self.start[0]:
            for row in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(row, self.start[1]))


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = [
            Ship(ship_coordinates[0], ship_coordinates[1])
            for ship_coordinates in ships
        ]
        self.field = {}
        for ship in self.ships:
            for deck in ship.decks:
                self.field[deck.row, deck.column] = ship

    def fire(self, location: tuple[int, int]) -> str:
        if location in self.field:
            self.field[location].fire(location[0], location[1])
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for cor_x in range(10):
            for cor_y in range(10):
                if (cor_x, cor_y) in self.field:
                    ship = self.field[(cor_x, cor_y)]
                    ship_deck = ship.get_deck(cor_x, cor_y)
                    if ship.is_drowned:
                        print("X" + " ", end="")
                    elif not ship_deck.is_alive:
                        print("*" + " ", end="")
                    else:
                        print("\u25A1" + " ", end="")
                else:
                    print("~" + " ", end="")
            print()
