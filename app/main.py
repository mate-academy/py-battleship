from typing import List


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return f"({self.row}, {self.column})"


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.decks = self.set_up(start, end)
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    @staticmethod
    def set_up(start: tuple, end: tuple) -> List[Deck]:
        length = (end[0] - start[0] + end[1] - start[1]) + 1
        decks = []
        for i in range(length):
            if end[0] > end[1]:
                decks.append(Deck(start[0] + i, start[1]))
            else:
                decks.append(Deck(start[0], start[1] + i))
        return decks

    def fire(self, row: int, column: int) -> None:
        fire = self.get_deck(row, column)
        if fire:
            fire.is_alive = False
            i = 0
            for deck in self.decks:
                if deck.is_alive is True:
                    i += 1
            if i == 0:
                self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        field = {}
        for coord in ships:
            ship = Ship(*coord)
            for deck in ship.decks:
                field[(deck.row, deck.column)] = ship
        self.field = field

    def _validate_field(self) -> str:
        ships = list({ship for ship in self.field.values()})
        sizes = []
        for i, uniq_ship in enumerate(ships):
            sizes.append(len(uniq_ship.decks))
            for deck in uniq_ship.decks:
                x, y = deck.row, deck.column
                tests = [
                    (x, y + 1), (x, y - 1), (x + 1, y),
                    (x - 1, y), (x + 1, y + 1), (x - 1, y + 1),
                    (x + 1, y - 1), (x - 1, y - 1)
                ]
                for test in tests:
                    x, y = test
                    if 0 <= x < 10 and 0 <= y < 10:
                        for index in range(i + 1, 9):
                            if ships[index].get_deck(x, y):
                                return (f"Ship with coordinates "
                                        f"x: {x}, y: {y} is in wrong position")
        correct_sizes = all(
            (sizes.count(1) == 4, sizes.count(2) == 3,
             sizes.count(3) == 2, sizes.count(4) == 1)
        )
        if correct_sizes:
            return "Input is validate"
        return "Wrong amount of ships"

    def print_field(self) -> None:
        for i in range(10):
            line = ""
            for index in range(10):
                ship = self.field.get((i, index))
                if ship:
                    deck = ship.get_deck(i, index)
                    if not ship.is_drowned:
                        if deck.is_alive:
                            line += "\u25A1 "
                        else:
                            line += "* "
                    else:
                        line += "x "
                else:
                    line += "~ "
            print(line)

    def fire(self, location: tuple) -> str:
        ship = self.field.get(location)
        if ship:
            deck = ship.get_deck(*location)
            ship.fire(*location)
            if deck:
                deck.is_alive = False
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"
