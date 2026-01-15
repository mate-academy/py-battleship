class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self.create_decks()

    def create_decks(self) -> list[Deck]:
        start_row, start_column = self.start
        end_row, end_column = self.end
        if start_row == end_row:
            return [
                Deck(start_row, current_column)
                for current_column in range(start_column, end_column + 1)
            ]
        return [
            Deck(current_row, start_column)
            for current_row in range(start_row, end_row + 1)
        ]

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def check_if_drowned(self) -> None:
        for deck in self.decks:
            if deck.is_alive:
                return
        self.is_drowned = True

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            self.check_if_drowned()


class Battleship:
    def __init__(self, ships: list[tuple[tuple]]) -> None:
        self.field = {}

        for ship in ships:
            start, end = ship
            start_row, start_column = start
            end_row, end_column = end
            ship_instance = Ship(start, end)
            if start_row == end_row:
                for current_column in range(start_column, end_column + 1):
                    self.field[(start_row, current_column)] = ship_instance
            else:
                for current_row in range(start_row, end_row + 1):
                    self.field[(current_row, start_column)] = ship_instance

        if not self._validate_field():
            raise ValueError("Invalid field configuration")

    def fire(self, location: tuple[int, int]) -> str:
        if location not in self.field:
            return "Miss!"

        ship = self.field[location]
        ship.fire(*location)
        return "Sunk!" if ship.is_drowned else "Hit!"

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                ship = self.field.get((row, column))
                if not ship:
                    print("~", end="")
                    continue

                deck = ship.get_deck(row, column)
                if deck.is_alive:
                    print(u"\u25A1", end="")
                elif ship.is_drowned:
                    print("x", end="")
                else:
                    print("*", end="")

            print()

    def _validate_field(self) -> bool:
        ships = list(set(self.field.values()))
        if len(ships) != 10:
            print(f"The total number of the ships should be 10, "
                  f"but got {len(ships)} instead")
            return False

        single_deck, double_deck, three_deck, four_deck = [0, 0, 0, 0]
        for ship in ships:
            decks = len(ship.decks)
            if decks == 1:
                single_deck += 1
            elif decks == 2:
                double_deck += 1
            elif decks == 3:
                three_deck += 1
            elif decks == 4:
                four_deck += 1
        wrong = 0
        if single_deck != 4:
            print(f"Field should have 4 single-deck ships, "
                  f"but got {single_deck} instead")
            wrong += 1
        if double_deck != 3:
            print(f"Field should have 3 double-deck ships, "
                  f"but got {double_deck} instead")
            wrong += 1
        if three_deck != 2:
            print(f"Field should have 2 three-deck ships, "
                  f"but got {three_deck} instead")
            wrong += 1
        if four_deck != 1:
            print(f"Field should have 1 four-deck ship, "
                  f"but got {four_deck} instead")
            wrong += 1
        if wrong > 0:
            return False

        for deck_location, ship in self.field.items():
            current_row, current_column = deck_location
            for row in range(current_row - 1, current_row + 2):
                for column in range(current_column - 1, current_column + 2):
                    neighbor_location = (row, column)
                    if (
                            0 <= row <= 9
                            and 0 <= column <= 9
                            and neighbor_location != deck_location
                    ):
                        neighbor = self.field.get(neighbor_location)
                        if neighbor and neighbor is not ship:
                            print("Ships shouldn't be located "
                                  "in the neighboring cells "
                                  "(even if cells are neighbors by diagonal)")
                            return False
        return True
