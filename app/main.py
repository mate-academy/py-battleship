from collections import defaultdict


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
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
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = [
            Deck(row, column)
            for row in range(self.start[0], self.end[0] + 1)
            for column in range(self.start[1], self.end[1] + 1)
        ]

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        if not any([deck.is_alive for deck in self.decks]):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = [Ship(*ship_location) for ship_location in ships]
        self.field = {
            (row, column): ship
            for ship in self.ships
            for row in range(ship.start[0], ship.end[0] + 1)
            for column in range(ship.start[1], ship.end[1] + 1)
        }

    def fire(self, location: tuple[int, int]) -> str:
        if location in self.field:
            ship = self.field[location]
            ship.fire(*location)
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def validate_field(self) -> None:
        if not len(set(ship for ship in self.field.values())) == 10:
            raise ValueError("The total number of ships should be 10")
        all_ships_decks_count = {
            (ship.start, ship.end): len(ship.decks)
            for ship in set(self.field.values())
        }
        decks_count = defaultdict(int)
        for decks in all_ships_decks_count.values():
            decks_count[decks] += 1

        if not decks_count == {1: 4, 2: 3, 3: 2, 4: 1}:
            raise ValueError("There should exactly be: \n"
                             "4 single-deck ships\n"
                             "3 double-deck ships\n"
                             "2 three-deck ships\n"
                             "1 four-deck ship")

    def print_field(self) -> None:
        field = [["~" for _ in range(10)] for _ in range(10)]
        for row, column in self.field:
            field[row][column] = u"\u25A1"
            ship = self.field[(row, column)]
            if ship.is_drowned:
                for deck in ship.decks:
                    field[deck.row][deck.column] = "X"
            else:
                for deck in ship.decks:
                    if not deck.is_alive:
                        field[deck.row][deck.column] = "*"
        for row in field:
            print(" ".join("{:<3}".format(cell) for cell in row))
