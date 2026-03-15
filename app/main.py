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
            is_drowned: bool = False
    ) -> None:
        self.decks = []
        self.is_drowned = is_drowned
        for i in range(
                max(
                    (end[0] - start[0]),
                    (end[1] - start[1])
                ) + 1
        ):
            if start[0] != end[0]:
                self.decks.append(Deck(start[0] + i, start[1]))
            elif start[1] != end[1]:
                self.decks.append(Deck(start[0], start[1] + i))
            else:
                self.decks.append(Deck(start[0], start[1]))

    def get_deck(
            self,
            row: int,
            column: int
    ) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(
            self,
            row: int,
            column: int
    ) -> None:
        deck = self.get_deck(row, column)
        if deck.is_alive:
            deck.is_alive = False
        if all(deck.is_alive is False for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(
            self,
            ships: list,
    ) -> None:
        self.field = {}
        for ship in ships:
            current_ship = Ship(ship[0], ship[1])
            for deck in current_ship.decks:
                self.field[deck.row, deck.column] = current_ship
        self._validate_field()

    def fire(
            self,
            location: tuple
    ) -> str:
        if location in self.field:
            self.field[location].fire(location[0], location[1])
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        field = [["~"] * 10 for _ in range(10)]
        for (row, column), ship in self.field.items():
            deck = ship.get_deck(row, column)
            if ship.is_drowned:
                field[row][column] = "x"
            elif not deck.is_alive:
                field[row][column] = "*"
            else:
                field[row][column] = u"\u25A1"
        for row in field:
            print(" ".join(row))

    def _validate_field(self) -> None:
        if len(set(self.field.values())) != 10:
            raise Exception("Invalid number of ships")
        ships_lengths = []
        for ship in set(self.field.values()):
            ships_lengths.append(len(ship.decks))
        if ships_lengths.count(1) != 4:
            raise Exception("Invalid number of ships")
        if ships_lengths.count(2) != 3:
            raise Exception("Invalid number of ships")
        if ships_lengths.count(3) != 2:
            raise Exception("Invalid number of ships")
        if ships_lengths.count(4) != 1:
            raise Exception("Invalid number of ships")
        for (row, column), ship in self.field.items():
            for deck_row in range(-1, 2):
                for deck_column in range(-1, 2):
                    if deck_row == 0 and deck_column == 0:
                        pass
                    elif (row + deck_row, column + deck_column) in self.field:
                        near_ship = self.field[
                            row + deck_row, column + deck_column
                        ]
                        if near_ship != ship:
                            raise Exception("Invalid location of ships")
