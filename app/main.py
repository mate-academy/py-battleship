from typing import Dict, List, Tuple, Union


class Deck:
    def __init__(
            self,
            row: int,
            column: int,
            is_alive: bool = True,
            is_hit: bool = False
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive
        self.is_hit = is_hit

    def fire(self) -> None:
        self.is_alive = False


class Ship:
    def __init__(
            self,
            start: Tuple[int, int],
            end: Tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        (start_row, start_column), (end_row, end_column) = start, end

        for row in range(start_row, end_row + 1):
            for column in range(start_column, end_column + 1):
                deck = Deck(row, column)
                self.decks.append(deck)

    def get_deck(self, row: int, column: int) -> Union[Deck, None]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck is not None:
            deck.fire()
            if not self.is_drowned and all(not d.is_alive for d in self.decks):
                self.is_drowned = True


class Battleship:
    def __init__(
            self,
            ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        self.field: Dict[Tuple[int, int], Ship] = {}
        for ship in ships:
            (start_row, start_column), (end_row, end_column) = ship
            new_ship = Ship(*ship)
            for row in range(start_row, end_row + 1):
                for column in range(start_column, end_column + 1):
                    self.field[(row, column)] = new_ship

    def fire(self, ceil: Tuple[int, int]) -> str:
        if ceil in self.field:
            ship = self.field[ceil]
            deck = ship.get_deck(*ceil)
            deck.is_hit = True
            if deck.is_alive:
                deck.fire()
                if all(not d.is_alive for d in ship.decks):
                    ship.is_drowned = True
                    return "Sunk!"
                return "Hit!"
            return "You already fired here!"
        return "Miss!"

    def print_field(self) -> None:
        table = ""
        for row in range(10):
            for column in range(10):
                location = (row, column)
                if location in self.field:
                    ship = self.field[location]
                    deck = ship.get_deck(row, column)
                    if deck.is_alive:
                        if deck.is_hit:
                            table += "*"
                        else:
                            table += u"\u25A1"
                    else:
                        table += "x"
                else:
                    table += "~"
                table += " "
            table += "\n"

        print(table)
