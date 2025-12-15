from typing import List


class Deck:
    def __init__(self,
                 row: int,
                 column: int,
                 is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False) -> None:
        self.decks = []
        self.is_drowned = is_drowned
        if start == end:
            self.decks.append(Deck(start[0], start[1]))
        elif start[0] < end[0]:
            for i in range(start[0], end[0] + 1):
                self.decks.append(Deck(i, start[1]))
        elif start[0] > end[0]:
            for i in range(start[0], end[0] - 1, -1):
                self.decks.append(Deck(i, start[1]))
        elif start[1] < end[1]:
            for i in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], i))
        else:
            for i in range(start[1], end[1] - 1, -1):
                self.decks.append(Deck(start[0], i))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if (row, column) == (deck.row, deck.column):
                return deck
        return None

    def get_ship_decks(self) -> List[Deck]:
        result = []
        for deck in self.decks:
            result.append((deck.row, deck.column))
        return result

    def fire(self, row: int, column: int) -> None:
        deck_hit = self.get_deck(row, column)
        if deck_hit.is_alive:
            deck_hit.is_alive = False
        decks_of_ship = []
        for deck in self.decks:
            decks_of_ship.append(deck.is_alive)
        if not any(decks_of_ship):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: List[tuple]) -> None:
        self.field = {}
        for ship in ships:
            new_ship = Ship(ship[0], ship[1])
            for deck in new_ship.get_ship_decks():
                self.field.update({deck: new_ship})
        if not self._validate_field():
            print("Wrong ships provided!!!")

    def fire(self, location: tuple) -> str:
        if location not in self.field.keys():
            return "Miss!"
        ship = self.field[location]
        ship.fire(location[0], location[1])
        if ship.is_drowned:
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        print("\nBATTLESHIP:\n")
        for row in range(0, 10):
            row_to_print = ""
            for column in range(0, 10):
                if (row, column) in self.field.keys():
                    ship = self.field[(row, column)]
                    if ship.is_drowned:
                        row_to_print += " x "
                        continue
                    if not ship.is_drowned:
                        deck = ship.get_deck(row, column)
                        if deck.is_alive:
                            row_to_print += " □ "
                            continue
                        if not deck.is_alive:
                            row_to_print += " * "
                            continue
                row_to_print += " ~ "
            print(row_to_print)

    def _validate_field(self) -> bool:
        ships = set()
        one_ships = 4
        two_ships = 3
        three_ships = 2
        four_ships = 1
        for ship in self.field.values():
            ships.add(ship)
            if len(ship.get_ship_decks()) == 1:
                one_ships -= 1
            if len(ship.get_ship_decks()) == 2:
                two_ships -= 1
            if len(ship.get_ship_decks()) == 3:
                three_ships -= 1
            if len(ship.get_ship_decks()) == 4:
                four_ships -= 1
        if len(ships) != 10:
            return False
        if (
                one_ships != 0
                and two_ships != 0
                and three_ships != 0
                and four_ships != 0
        ):
            return False
        return True
