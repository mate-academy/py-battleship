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
    decks = []

    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:

        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.length = None
        self.length_of_ship()
        self.create_decker()

    def length_of_ship(self) -> None:
        self.length = max(
            self.end[1] - self.start[1], self.end[0] - self.start[0]
        ) + 1

    def create_decker(self) -> None:
        if self.start[0] == self.end[0]:
            column = self.start[1]
            while True:
                if column > self.end[1]:
                    break
                self.decks.append(Deck(self.start[0], column))
                column += 1
        elif self.start[1] == self.end[1]:
            row = self.start[0]
            while True:
                if row > self.end[0]:
                    break
                self.decks.append(Deck(row, self.start[1]))
                row += 1

    def get_deck(self, row: int, column: int) -> str:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return self.fire(deck)

    def fire(self, deck: Deck) -> str:
        if self.is_drowned is False:
            deck.is_alive = False
            self.length -= 1
            if self.length == 0:
                self.is_drowned = True
                return "Sunk!"
            return "Hit!"
        return "Miss!"


class Battleship:
    field = {}

    def __init__(self, ships: tuple) -> None:
        self.ships = ships
        self.field.update({ship: Ship(ship[0], ship[1]) for ship in ships})
        self._validate_field()

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise Exception("the total number of the ships should be 10")
        length_ships = [self.field[ship].length for ship in self.field]
        if length_ships.count(4) != 1:
            raise Exception("there should be 1 four-deck ship")
        if length_ships.count(3) != 2:
            raise Exception("there should be 2 three-deck ships")
        if length_ships.count(2) != 3:
            raise Exception("there should be 3 double-deck ships")
        if length_ships.count(1) != 4:
            raise Exception("there should be 4 single-deck ships")
        neighboring_cells = [ship for ship in self.field]
        for cell in neighboring_cells:
            for check in neighboring_cells:
                if cell == check:
                    continue
                if cell[0][0] == cell[1][0] \
                        and cell[0][0] == check[0][0] == check[1][0]:
                    if cell[0][1] == check[0][1] \
                            or cell[0][1] == check[0][1] + 1:
                        raise Exception(
                            "ships shouldn't be located"
                            " in the neighboring cells"
                        )
                    if cell[1][1] == check[0][1] \
                            or cell[1][1] == check[0][1] - 1:
                        raise Exception(
                            "ships shouldn't be located"
                            " in the neighboring cells"
                        )
                if cell[0][1] == cell[1][0] \
                        and cell[0][1] == check[0][1] == check[1][1]:
                    if cell[0][0] == check[0][0] \
                            or cell[0][0] == check[0][0] + 1:
                        raise Exception(
                            "ships shouldn't be located"
                            " in the neighboring cells"
                        )
                    if cell[0][0] == check[0][0] \
                            or cell[0][0] == check[0][0] - 1:
                        raise Exception(
                            "ships shouldn't be located"
                            " in the neighboring cells"
                        )

    def fire(self, location: tuple) -> str:
        for ship in self.field:
            row, column = location[0], location[1]
            if row == ship[0][0] and row == ship[1][0]:
                if ship[1][1] >= column >= ship[0][1]:
                    return self.field[ship].get_deck(row, column)
            if column == ship[0][1] and column == ship[1][1]:
                if ship[1][0] >= row >= ship[0][0]:
                    return self.field[ship].get_deck(row, column)
        return "Miss!"

    def print_field(self) -> None:
        battle_field = ["~"] * 10
        for cell in range(len(battle_field)):
            for deck in Ship.decks:
                if deck.row == cell and deck.is_alive:
                    battle_field[deck.column] = "\u25A1"
                if deck.row == cell and deck.is_alive is False:
                    battle_field[deck.column] = "*"
            for ship in self.field.values():
                if ship.start[0] == cell and ship.is_drowned:
                    number = ship.end[1]
                    while True:
                        if number < ship.start[1]:
                            break
                        battle_field[number] = "X"
                        number -= 1
            print(" ".join(battle_field))
            battle_field = ["~"] * 10
