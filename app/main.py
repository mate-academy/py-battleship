class IncorrectNumberOfShips(Exception):
    def __str__(self) -> str:
        return "The total number of the ships should be 10"


class IncorrectShipCoordinates(Exception):
    def __str__(self) -> str:
        return ("The ends of the ship must lie on the same"
                " line and its length must not exceed 4 cells")


class IncorrectSetOfShips(Exception):
    def __str__(self) -> str:
        return ("there should be 4 single-deck, 3 double-deck,"
                " 2 three-deck and 1 four-deck ship")


class IncorrectPositionOfShips(Exception):
    def __str__(self) -> str:
        return ("Ships shouldn't be located in the neighboring cells"
                " (even if cells are neighbors by diagonal).")


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        self.decks = []
        if start[0] == end[0]:
            for index in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], index))
        else:
            for index in range(start[0], end[0] + 1):
                self.decks.append(Deck(index, start[1]))
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        is_drowned = True
        for deck in self.decks:
            if deck.is_alive is True:
                is_drowned = False
        if is_drowned:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        self._validate_field(ships)

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            self.print_field()
            return "Miss!"
        self.field[location].fire(location[0], location[1])
        self.print_field()
        if self.field[location].is_drowned:
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        for row in range(10):
            string = ""
            for column in range(10):
                if (row, column) not in self.field:
                    string += "~\t"
                else:
                    if self.field[(row, column)].get_deck(row,
                                                          column).is_alive:
                        string += u"\u25A1\t"
                    else:
                        if self.field[(row, column)].is_drowned:
                            string += "x\t"
                        else:
                            string += "*\t"
            print(string)
        print("")

    def _validate_field(self, ships: list) -> None:
        if len(ships) != 10:
            raise IncorrectNumberOfShips
        number_of_ships = {1: 0, 2: 0, 3: 0, 4: 0}
        for ship in ships:
            if ship[0][0] != ship[1][0] and ship[0][1] != ship[1][1]:
                raise IncorrectShipCoordinates
            ship_instance = Ship(ship[0], ship[1])
            ship_len = len(ship_instance.decks)
            if ship_len > 4:
                raise IncorrectShipCoordinates
            number_of_ships[len(ship_instance.decks)] += 1
            for deck in ship_instance.decks:
                self.field[(deck.row, deck.column)] = ship_instance
        if not (number_of_ships[1] == 4
                and number_of_ships[2] == 3
                and number_of_ships[3] == 2
                and number_of_ships[4] == 1):
            raise IncorrectSetOfShips
        for deck in self.field:
            for row_neighbourhood in [-1, 0, 1]:
                for column_neighbourhood in [-1, 0, 1]:
                    neighbourhood = (deck[0] + row_neighbourhood,
                                     deck[1] + column_neighbourhood)
                    if (neighbourhood in self.field
                            and self.field[deck] != self.field[neighbourhood]):
                        raise IncorrectPositionOfShips
