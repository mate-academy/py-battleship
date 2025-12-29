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
    def __init__(self, ships: List[Tuple[tuple[int]]]) -> None:
        self.field = {}
        for ship in ships:
            battle_ship = Ship(ship[0], ship[1])
            for deck in battle_ship.decks:
                self.field[deck] = battle_ship

    def fire(self, location: Tuple[int, int]) -> str:
        deck_dict = {(deck.row, deck.column): ship
                     for deck, ship in self.field.items()}
        if location in deck_dict:
            ship = deck_dict[(location[0], location[1])]
            ship.fire(location[0], location[1])

            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def _validate_field(self) -> None:
        ship_decks = [0, 0, 0, 0]
        ship_set = set(ship for ship in self.field.values())
        if len(ship_set) != 10:
            raise Exception("Total number of the ships must be 10")
        for ship in ship_set:
            if len(ship.decks) > 4:
                raise Exception("Abnormal length of the ship")
            ship_decks[len(ship.decks) - 1] += 1
        if ship_decks != [4, 3, 2, 1]:
            raise Exception("Please chose 4 single-deck ships, 3 double-deck "
                            "ships, 2 three-deck ships and 1 four-deck ship")


def print_field(battle_field: Battleship) -> None:
    field = [["~" for _ in range(0, 10)] for _ in range(0, 10)]

    for deck, ship in battle_field.field.items():
        if deck.is_alive:
            field[deck.row][deck.column] = u"\u25A1"
        else:
            if ship.is_drowned:
                field[deck.row][deck.column] = "x"
            else:
                field[deck.row][deck.column] = "*"

    for row in field:
        print(row)
