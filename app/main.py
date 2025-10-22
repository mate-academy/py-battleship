class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple[int, int],
                 end: tuple[int, int],
                 is_drowned: bool = False) -> None:
        self.decks = []
        if start[0] == end[0]:
            row = start[0]
            for col in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
                self.decks.append(Deck(row, col, is_alive=(not is_drowned)))
        else:
            col = start[1]
            for row in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
                self.decks.append(Deck(row, col, is_alive=(not is_drowned)))
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        counter = 0
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False
            if not deck.is_alive:
                counter += 1
        if counter == len(self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self,
                 ships: list[tuple[tuple[int, int], tuple[int, int]]]) -> None:
        self.field = {
            ship: Ship(ship[0], ship[1])
            for ship in ships
        }
        if not self._validate_field():
            self.field = {}
            print("Invalid field")

    def fire(self, location: tuple[int, int]) -> str:
        for ship in self.field.values():
            if ship.get_deck(*location) is not None:
                ship.fire(*location)
                if ship.is_drowned:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        printed_field = [
            [
                "~"
                for _ in range(10)
            ]
            for _ in range(10)
        ]
        for ship in self.field.values():
            for deck in ship.decks:
                if ship.is_drowned:
                    printed_field[deck.row][deck.column] = "x"
                if deck.is_alive:
                    printed_field[deck.row][deck.column] = u"\u25A1"
                else:
                    printed_field[deck.row][deck.column] = "*"
        for row in printed_field:
            print(" ".join(row))
            print()

    def _validate_field(self) -> bool:
        counter_single_deck_ships = 0
        counter_double_deck_ships = 0
        counter_three_deck_ships = 0
        counter_four_deck_ships = 0
        for ship_i in self.field.values():
            decks_i = ship_i.decks
            match len(decks_i):
                case 1:
                    counter_single_deck_ships += 1
                case 2:
                    counter_double_deck_ships += 1
                case 3:
                    counter_three_deck_ships += 1
                case 4:
                    counter_four_deck_ships += 1
            for ship_j in self.field.values():
                if ship_i == ship_j:
                    continue
                decks_j = ship_j.decks
                for deck_j in decks_j:
                    for deck_i in decks_i:
                        if (deck_i.row == deck_j.row
                                and deck_i.column == deck_j.column):
                            return False

                        row_diff = abs(deck_i.row - deck_j.row)
                        col_diff = abs(deck_i.column - deck_j.column)

                        if row_diff <= 1 and col_diff <= 1:
                            return False
        if (sum([counter_single_deck_ships,
                 counter_double_deck_ships,
                 counter_three_deck_ships,
                 counter_four_deck_ships]) == 10
                and counter_four_deck_ships == 1
                and counter_three_deck_ships == 2
                and counter_double_deck_ships == 3
                and counter_single_deck_ships == 4):
            return True
        else:
            return False
