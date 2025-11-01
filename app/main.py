class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False
                 ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned

        row_1, column_1 = self.start
        row_2, column_2 = self.end

        self.decks = []
        if row_1 == row_2 and column_1 != column_2:
            sorted_columns = sorted([column_1, column_2])
            column_1, column_2 = sorted_columns
            for column in range(column_1, column_2 + 1):
                self.decks.append(Deck(row_1, column))

        elif row_1 != row_2 and column_1 == column_2:
            sorted_rows = sorted([row_1, row_2])
            row_1, row_2 = sorted_rows
            for row in range(row_1, row_2 + 1):
                self.decks.append(Deck(row, column_1))

        elif row_1 == row_2 and column_1 == column_2:
            self.decks.append(Deck(row_1, column_1))

        else:
            raise ValueError("Ships only in rows or columns!")

    def get_deck(self, row: int, column: int) -> (Deck, None):
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        hit = False
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False
                if all(not deck.is_alive for deck in self.decks):
                    self.is_drowned = True
                    hit = True
                    print("Sunk!")
                else:
                    hit = True
                    print("Hit!")
        if hit is False:
            print("Miss!")


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = ships
        self.field = {}
        for ship in ships:
            ship_object = Ship(ship[0], ship[1])
            for deck in ship_object.decks:
                self.field[(deck.row, deck.column)] = ship_object

        self.array = [["~" for column in range(10)] for row in range(10)]
        for row, column in self.field.keys():
            self.array[row][column] = u"\u25A1"

        self._validate_field()

    def fire(self, location: tuple) -> str or None:

        row, column = location
        if not self.field.get((row, column)):
            return "Miss!"
        else:
            ship = self.field[(row, column)]

            deck = ship.get_deck(row, column)

            if not deck:
                return "Miss"

            if not deck.is_alive:
                return "Already hit!"

            deck.is_alive = False

            if all(deck.is_alive is False for deck in ship.decks):
                ship.is_drowned = True
                for deck in ship.decks:
                    self.array[deck.row][deck.column] = "x"
                return "Sunk!"
            else:
                self.array[row][column] = "*"
                return "Hit!"

    def print_field(self) -> None:

        for row in self.array:
            for column in row:
                print(column, end="     ")
            print("\n")

    def _validate_field(self) -> None:
        number_of_ships = len(self.ships)
        if number_of_ships != 10:
            raise ValueError("Total number of ships must be 10!")
        four_single_deck_ship = []
        three_two_deck_ship = []
        two_three_deck_ship = []
        one_four_deck_ship = []

        for ship in set(self.field.values()):
            if len(ship.decks) == 4:
                one_four_deck_ship.append(ship)
            elif len(ship.decks) == 3:
                two_three_deck_ship.append(ship)
            elif len(ship.decks) == 2:
                three_two_deck_ship.append(ship)
            elif len(ship.decks) == 1:
                four_single_deck_ship.append(ship)
            else:
                raise ValueError(
                    "Ship cannot be bigger than 4 decks"
                    " or smaller than 1 deck!"
                )

        if not len(four_single_deck_ship) == 4:
            raise ValueError("There should be 4 one deck ships.")
        if not len(three_two_deck_ship) == 3:
            raise ValueError("There should be 3 two decks ships.")
        if not len(two_three_deck_ship) == 2:
            raise ValueError("There should be 2 three decks ships.")
        if not len(one_four_deck_ship) == 1:
            raise ValueError("There should be 1 four decks ships.")

        occupied = set()

        for ship in self.ships:
            row_1, col_1 = ship[0]
            row_2, col_2 = ship[1]

            row_1, row_2 = sorted([row_1, row_2])
            col_1, col_2 = sorted([col_1, col_2])

            for row in range(max(0, row_1 - 1), min(10, row_2 + 2)):
                for col in range(max(0, col_1 - 1), min(10, col_2 + 2)):
                    if (row, col) in occupied:
                        raise ValueError(
                            "Field is occupied or too close to other ship!"
                        )

            for row in range(row_1, row_2 + 1):
                for col in range(col_1, col_2 + 1):
                    occupied.add((row, col))
