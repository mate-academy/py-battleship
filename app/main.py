class WrongInputData(Exception):
    pass


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:

        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []

        if self.start[0] == self.end[0]:
            self.decks.extend(
                [
                    Deck(self.start[0], i)
                    for i in range(self.start[1], self.end[1] + 1)
                ]
            )

        elif self.start[1] == self.end[1]:
            self.decks.extend(
                [
                    Deck(i, self.start[1])
                    for i in range(self.start[0], self.end[0] + 1)
                ]
            )

    def get_deck(self, row: int, column: int) -> Deck:

        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:

        deck = self.get_deck(row, column)
        deck.is_alive = False

        if not any(deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = ships
        self.field = {ship: Ship(ship[0], ship[1]) for ship in self.ships}
        self.print_field()  # I want to print a field as soon as I create it
        self._validate_field()

    def fire(self, location: tuple) -> str:

        for ship in self.field.values():
            if location in [(deck.row, deck.column) for deck in ship.decks]:
                ship.fire(location[0], location[1])
                if ship.is_drowned is True:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        field = [["~"] * 10 for _ in range(10)]

        for ship in self.field.values():
            if ship.is_drowned is True:
                for deck in ship.decks:
                    field[deck.row][deck.column] = "x"
            else:
                for deck in ship.decks:
                    if deck.is_alive is False:
                        field[deck.row][deck.column] = "*"
                    else:
                        field[deck.row][deck.column] = u"\u25A1"

        for line in field:
            print(line)

    def _validate_field(self) -> None:
        all_decks = [
            (deck.row, deck.column)
            for ship in self.field.values() for deck in ship.decks
        ]

        returns = []
        for ship in self.field.values():
            ship_decks = (
                all_decks[:len(all_decks) - (len(all_decks) - len(ship.decks))]
            )
            all_decks = all_decks[len(ship.decks):]

            for deck in ship_decks:
                returns.append(
                    self.is_obj_in_decks(
                        (deck[0] + 1, deck[1]), all_decks
                    )
                    or self.is_obj_in_decks(
                        (deck[0], deck[1] + 1), all_decks
                    )
                    or self.is_obj_in_decks(
                        (deck[0] - 1, deck[1]), all_decks
                    )
                    or self.is_obj_in_decks(
                        (deck[0], deck[1] - 1), all_decks
                    )
                    or self.is_obj_in_decks(
                        (deck[0] + 1, deck[1] + 1), all_decks
                    )
                    or self.is_obj_in_decks(
                        (deck[0] - 1, deck[1] - 1), all_decks
                    )
                    or self.is_obj_in_decks((
                        deck[0] - 1, deck[1] + 1), all_decks
                    )
                    or self.is_obj_in_decks(
                        (deck[0] + 1, deck[1] - 1), all_decks
                    )
                )

        if (
                (len(self.field) < 10)
                or (not self.count_check(4, 1))
                or (not self.count_check(3, 2))
                or (not self.count_check(2, 3))
                or (not self.count_check(1, 4))
                or any(returns)
        ):
            raise WrongInputData(
                "There is an issue with input data\n"
                "Please, follow all requirements:\n"
                "1. the total number of the ships should be 10;\n"
                "2. there should be 4 single-deck ships;\n"
                "3. there should be 3 double-deck ships;\n"
                "4. there should be 2 three-deck ships;\n"
                "5. there should be 1 four-deck ship;\n"
                "6. ships shouldn't be located in the neighboring cells\n"
                "(even if cells are neighbors by diagonal)."
            )

    def count_check(self, needed_len: int, needed_count: int) -> bool:
        count_of_decks = 0

        for ship in self.field.values():
            if len(ship.decks) == needed_len:
                count_of_decks += 1

        return count_of_decks == needed_count

    @staticmethod
    def is_obj_in_decks(obj: tuple, decks: list) -> bool:
        if obj in decks:
            return True

        return False
