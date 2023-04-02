
class Deck:
    def __init__(self, row: int, column: int,
                 is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple, end: tuple,
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.ships = []
        self.is_drowned = is_drowned
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.ships.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> object:
        for ship in self.ships:
            if (ship.row, ship.column) == (row, column):
                return ship

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        for deck in self.ships:
            self.is_drowned = True
            if deck.is_alive:
                self.is_drowned = False
                break


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = {}
        for ship in ships:
            boat = Ship(ship[0], ship[1])
            for deck in boat.ships:
                self.ships[(deck.row, deck.column)] = boat

    def fire(self, location: tuple) -> str:
        if location not in self.ships:
            return "Miss!"
        self.ships[location].fire(location[0], location[1])
        if self.ships[location].is_drowned:
            return "Sunk!"
        return "Hit!"
