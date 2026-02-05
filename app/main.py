from __future__ import annotations


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return f"Deck: row={self.row}, column={self.column}, " \
               f"is_alive={self.is_alive}"

    def __eq__(self, other: Deck | tuple) -> bool:
        if isinstance(other, Deck):
            if self.row == other.row and self.column == other.column:
                return True
            return False
        else:
            if self.row == other[0] and self.column == other[1]:
                return True
            return False


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False
                 ) -> None:
        self.decks = []
        self.is_drowned = is_drowned

        if start[0] == end[0]:
            temp = list(range(start[1], end[1] + 1))
            for temp_column in temp:
                self.decks.append(Deck(start[0], temp_column))
        elif start[1] == end[1]:
            temp = list(range(start[0], end[0] + 1))
            for temp_row in temp:
                self.decks.append(Deck(temp_row, end[1]))
        else:
            self.decks.append(Deck(start[0], start[1]))

    def __repr__(self) -> str:
        return f"Ship: {self.decks}, is_drowned={self.is_drowned}"

    def get_deck(self, row: int, column: int) -> Deck:
        return [deck
                for deck in self.decks
                if deck.row == row
                and deck.column == column
                ][0]

    def fire(self, row: int, column: int) -> None:
        if (row, column) in self.decks and self.is_drowned is False:
            index_of_deck = self.decks.index(Deck(row, column))

            if self.decks[index_of_deck].is_alive:
                self.decks[index_of_deck].is_alive = False

                counter = len(self.decks)
                for deck in self.decks:
                    if deck.is_alive is False:
                        counter -= 1
                if counter == 0:
                    self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}

        for some_ship in ships:
            ship = Ship(some_ship[0], some_ship[1])

            for temp_ship in ship.decks:
                self.field[(temp_ship.row, temp_ship.column)] = ship
        self._validate_field(ships)

    def _validate_field(self, ships: list) -> None:
        if len(ships) != 10:
            raise ValueError("the total number of the ships should be 10")

        counter_single_deck = 0
        counter_double_deck = 0
        counter_three_deck = 0
        counter_four_deck = 0
        ships = set(self.field.values())
        for ship in ships:
            if len(ship.decks) == 1:
                counter_single_deck += 1
            elif len(ship.decks) == 2:
                counter_double_deck += 1
            elif len(ship.decks) == 3:
                counter_three_deck += 1
            elif len(ship.decks) == 4:
                counter_four_deck += 1
        if counter_single_deck != 4:
            raise ValueError("there should be 4 single-deck ships")
        elif counter_double_deck != 3:
            raise ValueError("there should be 3 double-deck ships")
        elif counter_three_deck != 2:
            raise ValueError("there should be 2 three-deck ships")
        elif counter_four_deck != 1:
            raise ValueError("there should be 1 four-deck ship")

    def fire(self, location: tuple) -> str:
        if location in self.field.keys():
            temp_deck = Deck(location[0], location[1])
            index_of_deck = self.field[location].decks.index(temp_deck)

            self.field[location].fire(location[0], location[1])

            if self.field[location].is_drowned:
                return "Sunk!"
            elif not self.field[location].decks[index_of_deck].is_alive:
                return "Hit!"
        return "Miss!"
