from typing import List


class Deck:
    counter = 0

    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __str__(self) -> str:
        return f"Deck: {self.row} : {self.column}"


class Ship:

    def __init__(self, start: tuple, end: tuple,
                 is_drowned: bool = False) -> None:
        self.decks = self._decks_generator(start, end)
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck and deck.is_alive:
            deck.is_alive = False
        self.is_drowned = not any(deck.is_alive for deck in self.decks)

    @staticmethod
    def _decks_generator(start: tuple, end: tuple) -> list:
        start_row, start_column = start
        end_row, end_column = end
        if start_row == end_row:
            return [Deck(start_row, column)
                    for column in range(start_column, end_column + 1)]
        return [Deck(row, start_column)
                for row in range(start_row, end_row + 1)]


class Battleship:

    def __init__(self, ships: List[tuple]) -> None:
        self.field = self.get_field(ships)
        self._init_play_field()
        self.ship_count = {
            1: 0,
            2: 0,
            3: 0,
            4: 0
        }

    def _validate_fields(self) -> str:
        ships = self.field.values()

        for ship in ships:
            self.ship_count[len(ship.decks)] += 1

        for i in range(1, 5):
            if self.ship_count[i] != 5 - i:
                return f"You should have {5 - i} {i}-deck ships"

    def fire(self, location: tuple) -> str:
        ship = self.field.get(location)

        if ship:
            row, column = location
            ship.fire(row, column)
            self.play_field[row][column] = "*"
            if ship.is_drowned:
                for deck in ship.decks:
                    self.play_field[deck.row][deck.column] = "x"
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    @staticmethod
    def get_field(ships: List[tuple]) -> dict:
        field = {}
        ships = [Ship(start, end) for start, end in ships]
        for ship in ships:

            for deck in ship.decks:
                field[deck.row, deck.column] = ship

        return field

    def draw_play_field(self) -> None:
        print("\n".join(str(row) for row in self.play_field))

    def _init_play_field(self) -> None:
        self.play_field = [["~" for _ in range(10)] for _ in range(10)]
        for deck in self.field.keys():
            row, column = deck
            self.play_field[row][column] = "□"
