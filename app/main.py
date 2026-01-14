from typing import List


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self.create_deck(start, end)

    @staticmethod
    def create_deck(start: tuple, end: tuple) -> List[Deck]:
        return [
            Deck(row, column) for row in range(start[0], end[0] + 1)
            for column in range(start[1], end[1] + 1)
        ]

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if (deck.row, deck.column) == (row, column):
                return deck

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        self.is_drowned = True
        for deck in self.decks:
            if deck.is_alive:
                self.is_drowned = False
                break


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = ships
        self.field = {}
        for ship in ships:
            current_ship = Ship(ship[0], ship[1])
            for deck in current_ship.decks:
                self.field[(deck.row, deck.column)] = current_ship
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
        empty_cell = "~"
        alive_deck = u"\u25A1"
        hit_deck = "*"
        drowned_ship = "x"

        for row in range(0, 10):
            for column in range(0, 10):
                if (row, column) in self.field:
                    ship = self.field[(row, column)]
                    if ship.is_drowned:
                        print(drowned_ship, end="")
                    elif not ship.get_deck(row, column).is_alive:
                        print(hit_deck, end="")
                    else:
                        print(alive_deck, end="")
                else:
                    print(empty_cell, end="")
                print(" ", end="")
            print("")

    def _validate_field(self) -> None:
        ships = {
            1: 0,
            2: 0,
            3: 0,
            4: 0
        }
        for ship in self.field.values():
            ships[len(ship.decks)] += 1
        assert len(self.ships) == 10,\
            "The total number of the ships should be 10"
        assert ships[1] == 4,\
            "There should be 4 single-deck ships"
        assert ships[2] / 2 == 3,\
            "There should be 3 double-deck ships"
        assert ships[3] / 3 == 2,\
            "There should be 2 three-deck ships"
        assert ships[4] / 4 == 1,\
            "There should be 1 four-deck ships"
