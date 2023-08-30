from typing import List


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
        self, start: tuple, end: tuple, is_drowned: bool = False
    ) -> None:
        start_x, start_y = start
        end_x, end_y = end
        horizontal, vertical = (start_x - end_x, start_y - end_y)

        x, y = start  # noqa: VNE001

        if horizontal:
            coord_list = [
                (x, y + i) for i in range(abs(horizontal) + 1)
            ]  # noqa: VNE001
        elif vertical:
            coord_list = [
                (x, y + i) for i in range(abs(vertical) + 1)
            ]  # noqa: VNE001
        else:
            coord_list = [(x, y)]  # noqa: VNE001

        self.decks = []
        for x, y in coord_list:  # noqa: VNE001
            self.decks.append(Deck(x, y))  # noqa: VNE001

        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if (row, column) == (deck.row, deck.column):
                return deck

    def fire(self, row: int, column: int) -> str:
        if deck := self.get_deck(row, column):
            deck.is_alive = False

        if all(deck.is_alive is False for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: List[Ship]) -> None:
        self.field = {(x, y): None for x in range(10) for y in range(10)}

        for ship in ships:
            start, end = ship
            current_ship = Ship(start, end)

            for deck in current_ship.decks:
                self.field[deck.row, deck.column] = current_ship

    def fire(self, location: tuple) -> str:
        fire_result = "Miss!"

        if isinstance(self.field[location], Ship):
            self.field[location].fire(*location)
            fire_result = "Hit!"

            if self.field[location].is_drowned:
                fire_result = "Sunk!"

        return fire_result

    def print_field(self) -> None:
        for row in range(10):
            line = ""
            for col in range(10):
                if isinstance(self.field[(row, col)], Ship):
                    line += "\u25A1" + "\t"
                else:
                    line += "~\t"
            print(line)
