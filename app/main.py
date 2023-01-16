from typing import Tuple, List


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: Tuple[int],
            end: Tuple[int],
            is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned
        self.decks = []
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if (deck.row, deck.column) == (row, column):
                return deck

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        for deck in self.decks:
            self.is_drowned = True
            if deck.is_alive:
                self.is_drowned = False
                break


class Battleship:
    def __init__(self, ships: List[Tuple[tuple]]) -> None:
        self.field = {}
        for ship in ships:
            battle_ship = Ship(ship[0], ship[1])
            for deck in battle_ship.decks:
                self.field[(deck.row, deck.column)] = battle_ship

    def fire(self, location: Tuple[int]) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if location not in self.field:
            return "Miss!"
        self.field[location].fire(*location)
        if self.field[location].is_drowned:
            return "Sunk!"
        return "Hit!"

    def _validate_field(self) -> None:
        single, double, three, four = 0, 0, 0, 0
        ship_set = set(ship for ship in self.field.values())
        if len(ship_set) != 10:
            return "Total number of the ships must be 10"
        for ship in ship_set:
            if len(ship.decks) == 4:
                four += 1
            elif len(ship.decks) == 3:
                three += 1
            elif len(ship.decks) == 2:
                double += 1
            elif len(ship.decks) == 1:
                single += 1
            else:
                print("Abnormal length of the ship")
        if (single, double, three, four) != (4, 3, 2, 1):
            print("Please chose 4 single-deck ships, 3 double-deck ships, "
                  "2 three-deck ships and 1 four-deck ship")
