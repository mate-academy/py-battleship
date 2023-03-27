import numpy


class Deck:
    def __init__(self,
                 row: int,
                 column: int,
                 is_alive: bool = True,
                 deck_print: str = u"\u25A1") -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive
        self.deck_print = deck_print


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        if self.start[0] == self.end[0]:
            for i in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], i))
            return
        if self.start[1] == self.end[1]:
            for i in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(i, self.start[1]))
            return

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        fire_deck = self.get_deck(row, column)
        if fire_deck.is_alive:
            fire_deck.is_alive = False
            fire_deck.deck_print = "*"
        if not any([deck.is_alive for deck in self.decks]):
            self.is_drowned = True
            for deck in self.decks:
                deck.deck_print = "x"


class Battleship:

    def __init__(self, ships: list) -> None:
        self.battle_field = numpy.array([["~"] * 10] * 10)
        self.ships = ships
        self.field = {}
        for ship in self.ships:
            self.field[ship] = Ship(ship[0], ship[1])
        self._validate_field(self.field)

    def fire(self, location: tuple) -> str:
        for key, value in self.field.items():
            if (location[0] in range(key[0][0], key[1][0] + 1)
                    and location[1] in range(key[0][1], key[1][1] + 1)):
                value.fire(location[0], location[1])
                if value.is_drowned is True:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for values in self.field.values():
            for deck in values.decks:
                self.battle_field[deck.row][deck.column] = deck.deck_print
        print(self.battle_field)

    def _validate_field(self, ships: dict) -> None:
        if len(self.ships) != 10:
            raise ValueError("There must be exactly 10 ships on the field.")
        total_four_decks = 0
        total_three_decks = 0
        total_double_decks = 0
        total_single_decks = 0
        for ship in ships.values():
            if len(ship.decks) == 4:
                total_four_decks += 1
            elif len(ship.decks) == 3:
                total_three_decks += 1
            elif len(ship.decks) == 2:
                total_double_decks += 1
            elif len(ship.decks) == 1:
                total_single_decks += 1
            else:
                raise ValueError(f"Ship length {len(ship.decks)} is not valid."
                                 f"Ships must be 1-4 decks long.")

        if total_single_decks != 4:
            raise ValueError("There must be exactly 4 single-deck ships.")
        if total_double_decks != 3:
            raise ValueError("There must be exactly 3 double-deck ships.")
        if total_three_decks != 2:
            raise ValueError("There must be exactly 2 three-deck ships.")
        if total_four_decks != 1:
            raise ValueError("There must be exactly 1 four-deck ship.")
