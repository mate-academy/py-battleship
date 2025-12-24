class Deck:
    def __init__(self, row: int, column: int) -> None:
        self.row = row
        self.column = column
        self.is_alive = True


class Ship:
    def __init__(self, start: tuple, end: tuple) -> None:
        self.start = start
        self.end = end
        self.is_drowned = False
        self.decks = []

    def crate_decks(self, row: int, column: int) -> None:
        self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck.is_alive

    def fire(self, row: int, column: int) -> bool:
        health_ship = []

        for deck in self.decks:
            if deck.row != row or deck.column != column:
                health_ship.append(deck.is_alive)
            elif deck.row == row and deck.column == column:
                deck.is_alive = False
                health_ship.append(deck.is_alive)
        if not any(health_ship):
            self.is_drowned = False
            return self.is_drowned
        self.is_drowned = True
        return self.is_drowned


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = ships
        self.field = {}
        self.create_field_dict()
        self._validate_field()

    def create_field_dict(self) -> None:
        for ship in self.ships:
            instance_ship = Ship(ship[0], ship[1])
            for row in range(ship[0][0], ship[1][0] + 1):
                for column in range(ship[0][1], ship[1][1] + 1):
                    instance_ship.crate_decks(row, column)
                    self.field[row, column] = instance_ship

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"
        if location in self.field:
            get_location = self.field.get(location)
            if get_location.fire(location[0], location[1]):
                return "Hit!"
            return "Sunk!"

    def print_filed(self) -> None:
        matrix = []
        for _ in range(10):
            row = []
            for _ in range(10):
                row.append("-")
            matrix.append(row)

        for key, values in self.field.items():
            health_ship = []
            for deck in values.decks:
                health_ship.append(deck.is_alive)
            if any(health_ship):
                for deck in values.decks:
                    if deck.is_alive is True:
                        matrix[deck.row][deck.column] = "\u25A1"
                    if deck.is_alive is False:
                        matrix[deck.row][deck.column] = "*"
            else:
                for deck in values.decks:
                    matrix[deck.row][deck.column] = "x"

        for deck in matrix:
            print(deck)

    def _validate_field(self) -> None:
        count_ship = {
            "single_deck": 0,
            "double_deck": 0,
            "three_deck": 0,
            "four_deck": 0
        }

        for ship in self.ships:
            count_decks = (
                abs(ship[0][0] - ship[1][0])
                + abs(ship[0][1] - ship[1][1]) + 1
            )
            if count_decks == 4:
                count_ship["four_deck"] += 1
            if count_decks == 3:
                count_ship["three_deck"] += 1
            if count_decks == 2:
                count_ship["double_deck"] += 1
            if count_decks == 1:
                count_ship["single_deck"] += 1

        if sum(count_ship.values()) != 10:
            print(
                f"- Incorrect number of ships entered! "
                f"The total number of the ships should be 10.\n"
                f"There (is/are) {sum(count_ship.values())}.\n"
            )

        if count_ship["four_deck"] != 1:
            print(
                f"- Incorrect number of four-deck ship entered! "
                f"There should be 1 four-deck ship.\n"
                f"There are {count_ship['four_deck']} ships.\n"
            )

        if count_ship["three_deck"] != 2:
            print(
                f"- Incorrect number of three-deck ships entered! "
                f"There should be 2 three-deck ships.\n"
                f"There (is/are) {count_ship['three-deck']} ship(s).\n"
            )

        if count_ship["double_deck"] != 3:
            print(
                f"- Incorrect number of double-deck ships entered! "
                f"There should be 3 double-deck ships.\n"
                f"There (is/are) {count_ship['double_deck']} ship(s).\n"
            )

        if count_ship["single_deck"] != 4:
            print(
                f"- Incorrect number of single-deck ships entered! "
                f"There should be 4 single-deck ships.)\n"
                f"There (is/are) {count_ship['single_deck']} ship(s).\n"
            )

        fields = [[0 for _ in range(10)] for _ in range(10)]

        for index, ship in enumerate(self.ships, 1):
            for row_index in range(ship[0][0], ship[1][0] + 1):
                for column_index in range(ship[0][1], ship[1][1] + 1):
                    fields[row_index][column_index] = index

        for row in fields:
            for column in range(len(row) - 1):
                if row[column] != 0:
                    if row[column + 1] == 0 or row[column + 1] == row[column]:
                        continue
                    else:
                        print(f"There is an error in this line: {row}\n")
