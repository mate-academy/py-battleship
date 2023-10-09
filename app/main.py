from typing import Tuple, List


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.is_alive = is_alive
        self.coordinate = (row, column)


class Ship:
    def __init__(self,
                 start: Tuple[int, int],
                 end: Tuple[int, int],
                 is_drowned: bool = False) -> None:
        self.is_drowned = is_drowned
        self.decks = Ship.create_decks(start, end)

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.coordinate == (row, column):
                return deck

    def fire(self, row: int, column: int) -> str:
        self.get_deck(row, column).is_alive = False
        self.is_it_drowned()

        if self.is_drowned:
            return "Sunk!"
        return "Hit!"

    def is_it_drowned(self) -> None:
        self.is_drowned = not any([deck.is_alive for deck in self.decks])

    def get_length(self) -> int:
        return len(self.decks)

    @staticmethod
    def create_decks(ship_begin: Tuple[int, int],
                     ship_end: Tuple[int, int]) -> List:

        if ship_begin == ship_end:
            return [Deck(*ship_begin)]

        ship_decks = []

        for row in range(ship_begin[0], ship_end[0] + 1):
            for column in range(ship_begin[1], ship_end[1] + 1):
                ship_decks.append(Deck(row, column))

        return ship_decks


class Battleship:
    def __init__(self, ships: List[Tuple]) -> None:
        self._init_field(ships)
        self.print_field()

    def _init_field(self, ships: List[Tuple]) -> None:
        self.field = {}
        for ship in ships:
            temp_ship = Ship(*ship)
            for deck in temp_ship.decks:
                self.field[deck.coordinate] = temp_ship

    def fire(self, location: Tuple[int, int]) -> str:
        ship = self.field.get(location)
        if ship is not None:
            return ship.fire(*location)
        return "Miss!"

    def print_field(self) -> None:
        row = -1
        column = -1
        empty = " ~ "
        alive_deck = " □ "
        hit_deck = " * "
        drowned_ship = " x "

        def print_cell(coord: tuple) -> str:
            ship = coord
            if ship in self.field:
                if self.field[ship].is_drowned:
                    return drowned_ship
                elif not self.field[ship].get_deck(ship[0], ship[1]).is_alive:
                    return hit_deck
                elif self.field[ship].get_deck(ship[0], ship[1]).is_alive:
                    return alive_deck
            else:
                return empty

        for cell in range(100):
            if column == 9:
                column = -1
            if cell % 10 == 0:
                row += 1
                print()
            column += 1
            print(f" {print_cell((row, column))} ", end=" ")
