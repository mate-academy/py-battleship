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
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self.create_ship()

    def create_ship(self) -> list:
        ship = []
        if self.start == self.end:
            ship.append(Deck(self.start[0], self.start[1]))
        elif self.start[0] == self.end[0]:
            for num in range(self.start[1], self.end[1] + 1):
                ship.append(Deck(row=self.start[0], column=num))
        elif self.start[1] == self.end[1]:
            for num in range(self.start[0], self.end[0] + 1):
                ship.append(Deck(row=num, column=self.end[1]))
        else:
            raise ValueError("The ship should be vertical or horizontal")
        return ship

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> str:
        attacked_deck = self.get_deck(row, column)
        if not attacked_deck.is_alive:
            raise ValueError("The deck is already destroyed")
        attacked_deck.is_alive = False
        if all([deck.is_alive is False for deck in self.decks]):
            self.is_drowned = True
            return "Sunk!"
        else:
            return "Hit!"


class Battleship:
    def __init__(self, ships: list[tuple[tuple]]) -> None:
        self.__total_ships = []
        self.ships = ships
        self.field = self.create_field()
        self.battle_field = self.create_empty_field() | self.field
        self._validate()

    def create_field(self) -> dict:
        field = {}
        for start, end in self.ships:
            ship = Ship(start, end)
            if start == end:
                field[start] = ship
                self.__total_ships.append(1)
            elif start[0] == end[0]:
                for num in range(start[1], end[1] + 1):
                    field[(start[0], num)] = ship
                self.__total_ships.append((end[1] + 1) - start[1])
            elif start[1] == end[1]:
                for num in range(start[0], end[0] + 1):
                    field[(num, end[1])] = ship
                self.__total_ships.append((end[0] + 1) - start[0])
        return field

    @staticmethod
    def create_empty_field() -> dict:
        empty_field = {}
        for column in range(10):
            for row in range(10):
                empty_field[(column, row)] = "~"
        return empty_field

    def fire(self, location: tuple) -> str:
        if location not in self.battle_field:
            raise ValueError("The coordinate is out of the field")
        elif isinstance(self.battle_field[location], Ship):
            result = self.battle_field[location].fire(*location)
            return result
        else:
            return "Miss!"

    def _validate(self) -> None:
        if sorted(self.__total_ships) != [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]:
            raise ValueError("Incorrect number of ships.")
