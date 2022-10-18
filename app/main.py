from __future__ import annotations


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def get_deck(self) -> tuple:
        return self.row, self.column,


class Ship:
    def __init__(self, start: tuple, end: tuple,
                 is_drowned: bool = False) -> None:
        # Create decks and save them to a list `self.decks`
        self.decks = [Deck(start[0], start[1])]
        if start != end:
            index = 0 if start[0] != end[0] else 1
            current_deck = [*start]
            end_desk = [*end]
            while current_deck != end_desk:
                current_deck[index] += 1
                self.decks.append(Deck(current_deck[0], current_deck[1]))
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False
                break

        for deck in self.decks:
            if deck.is_alive:
                return

        self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.field = {}
        for ship_info in ships:
            ship = Ship(ship_info[0], ship_info[1])
            self._set_ship(ship)

    def _set_ship(self, ship: Ship) -> None:
        for deck in ship.decks:
            self.field[(deck.get_deck())] = ship

    def _validate_field(self) -> bool:
        ships = []
        valid_ships = {1: 0, 2: 0, 3: 0, 4: 0}
        for ship in self.field.values():
            if ship not in ships:
                valid_ships[len(ship.decks)] += 1
                ships.append(ship)

        is_valid = all((
            valid_ships[1] == 4,
            valid_ships[2] == 3,
            valid_ships[3] == 2,
            valid_ships[4] == 1
        ))
        return is_valid and self._validate_ship_location(ships)

    def _validate_ship_location(self, ships: list(Ship)) -> bool:
        for ship in ships:
            for desk in ship.decks:
                for index1 in range(-1, 2):
                    for index2 in range(-1, 2):
                        ship_test = self.field.get(
                            (desk.row + index1, desk.column + index2), None)
                        if ship_test is not None and ship != ship_test:
                            return False
        return True

    def validate(self) -> bool:
        return self._validate_field()

    def fire(self, location: tuple) -> None:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        ship = self.field.get(location, None)
        if ship is not None:
            ship.fire(*location)
            if ship.is_drowned:
                return "Sunk!"
            else:
                return "Hit!"
        return "Miss!"

    def draw_battleship(self) -> None:
        draw = []
        for index1 in range(10):
            row = ""
            for index2 in range(10):
                ship = self.field.get((index1, index2), None)
                if ship is None:
                    row += "\t~\t"
                elif ship.is_drowned:
                    row += "\tx\t"
                elif not ship.get_deck(index1, index2).is_alive:
                    row += "\t*\t"
                else:
                    row += u"\t\u25A1\t"
            draw.append(row)

        for row in draw:
            print(row)


if __name__ == "__main__":
    battle_ship = Battleship(
        ships=[
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
    )

    print(battle_ship.validate())
    battle_ship.draw_battleship()
    print(battle_ship.fire((7, 9)))
    battle_ship.draw_battleship()
    print(battle_ship.fire((2, 8)))
    print(battle_ship.fire((2, 9)))
    battle_ship.draw_battleship()
