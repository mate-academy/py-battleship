class ValidationInputDataError(Exception):
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

    def __str__(self) -> str:
        return f"deck: x={self.row}, y={self.column}, is_alive={self.is_alive}"


class Ship:
    def __init__(
            self,
            start: tuple[int],
            end: tuple[int],
            is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned
        if start[0] == end[0]:
            self.decks = [
                Deck(start[0], i)
                for i in range(start[1], end[1] + 1)
            ]
        if start[1] == end[1]:
            self.decks = [
                Deck(i, start[1])
                for i in range(start[0], end[0] + 1)
            ]

    def __repr__(self) -> str:
        return f"ship: {self.decks}, is_drowned={self.is_drowned}"

    def get_deck(self, row: int, column: int) -> None | Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        self.is_drowned = all([
            not deck.is_alive
            for deck in self.decks
        ])
        return "Sunk!" if self.is_drowned else "Hit!"


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {
            ship: Ship(ship[0], ship[1])
            for ship in ships
        }
        self._validate_field()

    def __str__(self) -> str:
        return f"{self.field}"

    def _validate_field(self) -> None:
        if len(self.field) != 10:
            raise ValidationInputDataError(
                "The total number of ships should be 10"
            )

        ships_count = {1: 0, 2: 0, 3: 0, 4: 0}
        for ship_start, ship_end in self.field.keys():
            ship_len = 1 + max(
                abs(ship_start[0] - ship_end[0]),
                abs(ship_start[1] - ship_end[1])
            )
            if ship_len > 4:
                raise ValidationInputDataError(
                    "The maximum length of the ship should not exceed 4 decks"
                )
            ships_count[ship_len] += 1

        if ships_count != {1: 4, 2: 3, 3: 2, 4: 1}:
            raise ValidationInputDataError(
                """There should be 4 single-deck ships
                There should be 3 double-deck ships
                There should be 2 three-deck ships
                There should be 1 four-deck ship"""
            )

        ship_deck_all = []
        for ship in self.field.keys():
            ship = sorted(ship)
            ship_deck = []
            for i in range(ship[0][0], ship[1][0] + 1):
                for k_ in range(ship[0][1], ship[1][1] + 1):
                    spase = [i, k_]
                    ship_deck.append(spase)
            ship_deck_all += ship_deck

        for ship in self.field.keys():
            ship = sorted(ship)
            y0 = ship[0][0] - 1 if ship[0][0] - 1 >= 0 else 0
            y1 = ship[1][0] + 1 if ship[1][0] + 1 <= 9 else 9
            x0 = ship[0][1] - 1 if ship[0][1] - 1 >= 0 else 0
            x1 = ship[1][1] + 1 if ship[1][1] + 1 <= 9 else 9
            ship_spase = []
            for i in range(y0, y1 + 1):
                for k_ in range(x0, x1 + 1):
                    spase = [i, k_]
                    ship_spase.append(spase)

            ship_deck = []
            for i in range(ship[0][0], ship[1][0] + 1):
                for k_ in range(ship[0][1], ship[1][1] + 1):
                    spase = [i, k_]
                    ship_deck.append(spase)

            for deck in ship_deck:
                ship_spase.remove(deck)

            for spase in ship_spase:
                if spase in ship_deck_all:
                    raise ValidationInputDataError(
                        "Ships shouldn't be located in the neighboring cells "
                        "(even if cells are neighbors by diagonal)."
                    )

    def fire(self, location: tuple) -> str:
        for coords, ship in self.field.items():
            ship_decks = ship.get_deck(location[0], location[1])
            if ship_decks is not None:
                return ship.fire(location[0], location[1])
        return "Miss!"

    def print_field(self) -> None:
        for i in range(0, 10):
            for k_ in range(0, 10):
                coord = (i, k_)
                for coords, ship in self.field.items():
                    deck = ship.get_deck(*coord)
                    if deck is not None:
                        if ship.is_drowned:
                            print("x ", end=" ")
                            break
                        if not deck.is_alive:
                            print("* ", end=" ")
                            break
                        print(u"\u25A1 ", end=" ")
                        break
                else:
                    print("~ ", end=" ")
            print()
        print()
