from typing import List, Dict, Tuple, Union


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
        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
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
            new_ship = Ship(ship[0], ship[1])
            for row in range(start_row, end_row + 1):
                for column in range(start_column, end_column + 1):
                    self.field[(row, column)] = new_ship

    def fire(self, ceil: Tuple[int, int]) -> str:
        if ceil in self.field:
            ship = self.field[ceil]
            deck = ship.get_deck(ceil[0], ceil[1])
            deck.is_hit = True
            if deck.is_alive:
                deck.fire()
                if all(not d.is_alive for d in ship.decks):
                    ship.is_drowned = True
                    return "Sunk!"
                else:
                    return "Hit!"
            else:
                return "You already fired here!"
        else:
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


ships = [
    ((0, 0), (0, 3)),
    ((0, 5), (0, 6)),
    ((0, 8), (0, 9)),
    ((2, 0), (4, 0)),
    ((2, 4), (2, 6)),
    ((2, 8), (2, 9)),
    ((9, 9), (9, 9)),
    ((7, 7), (7, 7)),
    ((7, 9), (7, 9)),
    ((9, 7), (9, 7)),
]

battle_ship = Battleship(ships)
battle_ship.fire((0, 4))
battle_ship.fire((0, 3))
battle_ship.fire((0, 2))
battle_ship.fire((0, 1))
battle_ship.fire((0, 0))
battle_ship.print_field()
