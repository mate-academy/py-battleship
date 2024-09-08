class WrongInputError(Exception):
    pass


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


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned

        if start[0] == end[0]:
            self.decks = [
                Deck(start[0], column)
                for column in range(start[1], end[1] + 1)
            ]
        elif start[1] == end[1]:
            self.decks = [
                Deck(row, start[1])
                for row in range(start[0], end[0] + 1)
            ]

    def get_deck(
            self,
            row: int,
            column: int
    ) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(
            self,
            row: int,
            column: int
    ) -> str:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        if not any(deck.is_alive for deck in self.decks):
            self.is_drowned = True
            return "Sunk!"
        return "Hit!"


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = ships
        self.not_validated_field = {}

        for ship in self.ships:
            new_ship = Ship(*ship)
            decks = tuple(
                [(deck.row, deck.column) for deck in new_ship.decks]
            )
            self.not_validated_field[decks] = new_ship

        if self._validate_field():
            self.field = self.not_validated_field

    def fire(self, location: tuple) -> str:
        for decks, ship in self.field.items():
            if location in decks:
                return ship.fire(*location)

        return "Miss!"

    def print_field(self) -> None:
        empty_field = [
            ["~" for _ in range(10)] for _ in range(10)
        ]
        print(empty_field)
        for ship in self.field.values():
            if not any(deck.is_alive for deck in ship.decks):
                for deck in ship.decks:
                    empty_field[deck.row][deck.column] = "x"
            else:
                for deck in ship.decks:
                    if deck.is_alive:
                        empty_field[deck.row][deck.column] = u"\u25A1"
                    else:
                        empty_field[deck.row][deck.column] = "*"

        for line in empty_field:
            print("    ".join(line))

    def check_neighbor_cells(self) -> bool | Exception:
        all_decks_by_ships = [
            list(deck) for deck in self.not_validated_field
        ]
        for index, ship in enumerate(all_decks_by_ships):
            decks_to_compare = all_decks_by_ships[:]
            decks_to_compare.remove(all_decks_by_ships[index])

            all_decks_copy = [
                deck for ship_decks in decks_to_compare
                for deck in ship_decks
            ]

            for deck in ship:
                for condition in (
                    (deck[0], deck[1] + 1),
                    (deck[0], deck[1] - 1),
                    (deck[0] + 1, deck[1]),
                    (deck[0] - 1, deck[1]),
                    (deck[0] - 1, deck[1] - 1),
                    (deck[0] + 1, deck[1] + 1),
                    (deck[0] - 1, deck[1] + 1),
                    (deck[0] + 1, deck[1] - 1)
                ):
                    if condition in all_decks_copy:
                        raise WrongInputError(
                            "Ships shouldn't be located "
                            "in the neighboring cells"
                        )
        return True

    def check_number_of_ships_by_len(
            self,
            number: int,
            length: int
    ) -> Exception | bool:
        ships_count = 0
        for ship in self.not_validated_field:
            if len(ship) == length:
                ships_count += 1
        if ships_count == number:
            return True

        raise WrongInputError(
            f"You should have {number} ship/s of length {length} !"
        )

    def check_ships_amount_equal_ten(self) -> bool | Exception:
        if len(self.ships) == 10:
            return True
        raise WrongInputError("You should input ten ships!")

    def _validate_field(self) -> bool | Exception:
        return (
            self.check_ships_amount_equal_ten()
            and all([self.check_number_of_ships_by_len(number, length)
                    for number, length in ((1, 4), (2, 3), (3, 2), (4, 1))])
        )
