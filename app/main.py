from app.custom_exceptions import (
    NumberOfShipsError,
    NumberOfTypesError,
    LocationError
)


class Deck:
    def __init__(
        self,
        row: int,
        column: int,
        is_alive: bool = True
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive
        Battleship.art_field[row][column] = "|" + u"\u25A1" + "|"


class Ship:
    def __init__(
        self,
        start: tuple,
        end: tuple,
        is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.decks: list[Deck]
        if end[0] == start[0]:
            self.decks = [
                Deck(start[0], start[1] + i)
                for i in range(end[1] - start[1] + 1)
            ]
        else:
            self.decks = [
                Deck(start[0] + i, start[1])
                for i in range(end[0] - start[0] + 1)
            ]
        self.is_drowned = is_drowned
        # Create decks and save them to a list `self.decks`

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if (
                deck.row == row
                and deck.column == column
            ):
                return deck
        # Find the corresponding deck in the list

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        Battleship.art_field[row][column] = " ##"
        if all([not deck.is_alive for deck in self.decks]):
            self.is_drowned = True
            for deck in self.decks:
                Battleship.art_field[deck.row][deck.column] = "<X>"
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed


class Battleship:

    art_field = [
        [" ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v"],
        [" ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v"],
        [" ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v"],
        [" ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v"],
        [" ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v"],
        [" ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v"],
        [" ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v"],
        [" ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v"],
        [" ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v"],
        [" ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v", " ^v"],
    ]

    def __init__(self, ships: list) -> None:
        self.field = {}
        self.ships = []
        for ship in ships:
            new_ship = Ship(ship[0], ship[1])
            self.ships.append(new_ship)
            for deck in new_ship.decks:
                self.field[(deck.row, deck.column)] = new_ship
        self._validate_field(self.ships)
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it

    def fire(self, location: tuple) -> str:
        if location in self.field.keys():
            self.field[location].fire(location[0], location[1])
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

        #  -------------------
        # |0 0 0 0 0 0 0 0 0 0|

        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.

    def print_field(self) -> None:
        print(" --------------------------------")
        for row in self.art_field:
            print("| " + "".join(row) + " |")
        print(" --------------------------------")
        print("\n")

    def _validate_field(self, ships: list) -> None:
        if len(ships) != 10:
            raise NumberOfShipsError(
                f"There should be 10 ships on the "
                f"battlefield. You have: {len(ships)}"
            )
        counter_deck = [0, 0, 0, 0]
        for ship in self.ships:
            if len(ship.decks) in range(1, 5):
                counter_deck[len(ship.decks) - 1] += 1
        for i in range(len(counter_deck)):
            if counter_deck[i] != len(counter_deck) - i:
                raise NumberOfTypesError(
                    f"There should be {len(counter_deck) - i}"
                    f" {i + 1}-deck ships. "
                    f"You have: {counter_deck[i]}."
                )
        for row, column in self.field.keys():
            check_deck = [-1, 0, 1]
            for i in check_deck:
                for j_i in check_deck:
                    if (row + i, column + j_i) in self.field.keys():
                        if (
                            self.field[(row + i, column + j_i)]
                            is not self.field[(row, column)]
                        ):
                            raise LocationError(
                                "Your ships are too "
                                "close to each other"
                            )


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


battle_ship.print_field()
battle_ship.fire((0, 0))
battle_ship.print_field()
battle_ship.fire((0, 1))
battle_ship.print_field()
battle_ship.fire((0, 2))
battle_ship.print_field()
battle_ship.fire((0, 3))
battle_ship.print_field()
