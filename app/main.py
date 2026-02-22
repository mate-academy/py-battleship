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
        self.is_drowned = is_drowned
        self.start = start
        self.end = end
        self.decks = [Deck(row, column)
                      for row in range(self.start[0], self.end[0] + 1)
                      for column in range(self.start[1], self.end[1] + 1)]

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            for deck in self.decks:
                if deck.is_alive:
                    return "Hit!"
            self.is_drowned = True
            return "Sunk!"


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = [Ship(*ship) for ship in ships]
        self.field = {}
        for ship in self.ships:
            for deck in ship.decks:
                self.field[deck.row, deck.column, ] = ship

    def _validate_field(self, ships: list) -> None:
        if len(ships) != 10:
            raise ValueError
        ship_1 = 0
        ship_2 = 0
        ship_3 = 0
        ship_4 = 0
        for ship in ships:
            if len(ship.decks) == 1:
                ship_1 += 1
            elif len(ship.decks) == 2:
                ship_2 += 1
            elif len(ship.decks) == 3:
                ship_3 += 1
            elif len(ship.decks) == 4:
                ship_4 += 1
        if ship_1 != 4 or ship_2 != 3 or ship_3 != 2 or ship_4 != 1:
            raise ValueError
        self.neighbor_cell = []
        for ship in ships:
            for i in range(ship[1][1] - ship[0][1] + 3):
                self.neighbor_cell.append((ship[0][0] - 1, ship[0][1] - 1 + i))
                self.neighbor_cell.append((ship[1][0] + 1, ship[1][1] - 1 + i))
            for i in range(ship[1][0] - ship[0][0] + 1):
                self.neighbor_cell.append((ship[0][0] + i, ship[1][0] - 1))
                self.neighbor_cell.append((ship[0][0] + i, ship[1][0] + 1))
        for cell in self.neighbor_cell:
            for ship in self.ships:
                for deck in ship.decks:
                    if cell == deck:
                        raise ValueError

    def fire(self, location: tuple) -> str:
        for coord, ship in list(self.field.items()):
            if location == coord:
                return ship.fire(*location)
        return "Miss!"
