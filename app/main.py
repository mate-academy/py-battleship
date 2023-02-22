from __future__ import annotations


class ErrorNumberOfTheShips(ValueError):
    pass


class ErrorNumberOfShipsDeck(ValueError):
    pass


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    @staticmethod
    def decks_maker(start: tuple, end: tuple) -> list[Deck]:
        decks = []
        if start[0] - end[0] != 0:
            for row in range(start[0], end[0] + 1):
                decks.append(Deck(row, end[1]))
        elif start[1] - end[1] != 0:
            for column in range(start[1], end[1] + 1):
                decks.append(Deck(start[0], column))
        elif start == end:
            decks.append(Deck(start[0], start[1]))

        return decks


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.decks = Deck.decks_maker(start, end)
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        alive = False
        for deck in self.decks:
            if deck.is_alive:
                alive = True
        if not alive:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = self.field_maker(ships)
        self._validate_field(self.field)
        self.field_picture = self.make_start_battle_map()

    def make_start_battle_map(self) -> list:
        battle_map = [["~" for _ in range(10)] for _ in range(10)]
        for ship_key in self.field:
            for row, column in ship_key:
                battle_map[row][column] = u"\u25A1"

        return battle_map

    def print_field(self) -> None:
        picture = ""
        for row in self.field_picture:
            picture += "  ".join(row) + "\n"
        print(picture)

    def fire_on_picture(self, row: int, column: int) -> None:
        self.field_picture[row][column] = "*"

    def make_sunk_ship_on_picture(self, ship_decks: tuple) -> None:
        for deck in ship_decks:
            self.field_picture[deck[0]][deck[1]] = "x"

    def fire(self, location: tuple) -> str:

        for ship_decks in self.field:
            if location in ship_decks:
                for deck in self.field[ship_decks].decks:
                    if location == (deck.row, deck.column):
                        self.fire_on_picture(deck.row, deck.column)
                        self.field[ship_decks].fire(deck.row, deck.column)
                        if self.field[ship_decks].is_drowned:
                            self.make_sunk_ship_on_picture(ship_decks)
                            self.print_field()
                            return "Sunk!"
                        self.print_field()
                        return "Hit!"
        self.print_field()
        return "Miss!"

    @staticmethod
    def field_maker(ships: list[tuple[tuple]]) -> dict:
        field = {}
        for start, end in ships:
            ship = Ship(start, end)
            field[tuple(
                [(deck.row, deck.column) for deck in ship.decks]
            )] = ship

        return field

    @staticmethod
    def _validate_field(ships: dict) -> None:
        if len(ships) != 10:
            raise ErrorNumberOfTheShips(
                "The total number of the ships should be 10")
        decks = [len(ships[key].decks) for key in ships]
        if decks.count(4) != 1:
            raise ErrorNumberOfShipsDeck("There should be 1 four-deck ship")
        if decks.count(3) != 2:
            raise ErrorNumberOfShipsDeck("There should be 2 three-deck ships")
        if decks.count(2) != 3:
            raise ErrorNumberOfShipsDeck("There should be 3 double-deck ships")
        if decks.count(1) != 4:
            raise ErrorNumberOfShipsDeck("There should be 4 single-deck ships")
