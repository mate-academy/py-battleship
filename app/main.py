class ShipValidationError(Exception):
    pass


class Deck:
    def __init__(self,
                 row: int,
                 column: int,
                 is_alive: bool = True
                 ) -> None:
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
        self.decks = []
        self.create_decks()

    def create_decks(self) -> None:
        if self.start == self.end:
            self.decks.append(Deck(self.start[0], self.start[1]))

        elif self.start[0] == self.end[0]:
            for column in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], column))

        elif self.start[1] == self.end[1]:
            for row in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(row, self.start[1]))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                return deck

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        if not any([deck.is_alive for deck in self.decks]):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = ships
        self.field = {}
        self.board = [["~"] * 10 for count in range(10)]
        self.field = {ship: Ship(ship[0], ship[1]) for ship in ships}

    def fire(self, location: tuple) -> str:
        for ship in self.field.values():
            if ship.get_deck(location[0], location[1]):
                ship.fire(location[0], location[1])
                if ship.is_drowned:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"

    def update_board_with_ships(self) -> list:
        for ship in self.field.values():
            for deck in ship.decks:
                self.board[deck.row][deck.column] = u"\u25A1"
        return self.board

    def update_board_with_shoots(self) -> list:
        self.update_board_with_ships()
        for ship in self.field.values():
            for deck in ship.decks:
                if not deck.is_alive:
                    self.board[deck.row][deck.column] = u"\u2612"
            if ship.is_drowned:
                for deck in ship.decks:
                    self.board[deck.row][deck.column] = "x"
        return self.board

    def print_board(self) -> None:
        for element in self.board:
            print(*element)

    def _validate_field(self) -> None:
        if len(self.field) != 10:
            raise ShipValidationError(
                "the total number of the ships should be 10"
            )

        len_of_ships = {1: 0, 2: 0, 3: 0, 4: 0}
        for ship in self.field.keys():
            if ship[0][0] != ship[1][0] and ship[0][1] != ship[1][1]:
                raise ShipValidationError(
                    "ships shouldn't be located diagonally"
                )
            elif ship[0] == ship[1]:
                len_of_ships[1] += 1
            elif ship[0][0] - ship[1][0] == -1 \
                    or ship[0][1] - ship[1][1] == -1:
                len_of_ships[2] += 1
            elif ship[0][0] - ship[1][0] == -2 \
                    or ship[0][1] - ship[1][1] == -2:
                len_of_ships[3] += 1
            elif ship[0][0] - ship[1][0] == -3 \
                    or ship[0][1] - ship[1][1] == -3:
                len_of_ships[4] += 1
        types_of_ship = ["single", "double", "three", "four"]
        for index, actual_deck_count in enumerate(len_of_ships.values()):
            if actual_deck_count != 4 - index:
                raise ShipValidationError(f"there should be {4-index}"
                                          f"{types_of_ship[index]}-deck ships")
