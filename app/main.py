class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple[int, int], end: tuple[int, int]) -> None:
        self.decks = [Deck(x_coord, y_coord)
                      for x_coord in range(start[0], end[0] + 1)
                      for y_coord in range(start[1], end[1] + 1)]
        self.alive_decks = len(self.decks)

    def get_deck(self, row: int, column: int) -> bool:
        for deck in self.decks:
            if (row, column) == (deck.row, deck.column):
                return deck.is_alive

    def fire(self, row: int, column: int) -> None:
        for deck in self.decks:
            if (row, column) == (deck.row, deck.column):
                deck.is_alive = False


class Battleship:
    def __init__(self,
                 ships: list[tuple[tuple[int, int], tuple[int, int]]]) -> None:

        ships = [Ship(*ship_coord) for ship_coord in ships]
        self.field = {(deck.row, deck.column): ship
                      for ship in ships for deck in ship.decks}
        if not self._validate_field(ships):
            print("List of ships is wrong!")

    def fire(self, location: tuple[int, int]) -> str:
        if location in self.field:
            if self.field[location].get_deck(*location):
                self.field[location].fire(*location)
                self.field[location].alive_decks -= 1
            if self.field[location].alive_decks == 0:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        print(end="  ")
        for column_num in range(10):
            print(f" {column_num} ", end="")
        print()
        for row in range(10):
            print(row, end=" ")
            for column in range(10):
                if (row, column) in self.field:
                    if self.field[(row, column)].get_deck(row, column):
                        print(u" \u25A1 ", end="")
                    else:
                        print(" x ", end="")
                else:
                    print(" . ", end="")
            print()

    def _validate_field(self, ships: list[Ship]) -> bool:
        single_deck = 0
        double_deck = 0
        three_deck = 0
        four_deck = 0
        for ship in ships:
            if ship.alive_decks == 4:
                four_deck += 1
            if ship.alive_decks == 3:
                three_deck += 1
            if ship.alive_decks == 2:
                double_deck += 1
            if ship.alive_decks == 1:
                single_deck += 1
        if (four_deck != 1 or three_deck != 2
                or double_deck != 3 or single_deck != 4):
            return False
        check_pool = []
        for ship in ships:
            for deck in ship.decks:
                if (deck.row, deck.column) in check_pool:
                    return False
            for deck in ship.decks:
                check_pool.extend([(deck.row, deck.column),
                                  (deck.row, deck.column + 1),
                                  (deck.row, deck.column - 1),
                                  (deck.row + 1, deck.column + 1),
                                  (deck.row + 1, deck.column - 1),
                                  (deck.row + 1, deck.column),
                                  (deck.row - 1, deck.column + 1),
                                  (deck.row - 1, deck.column - 1),
                                  (deck.row - 1, deck.column)])
        return True
