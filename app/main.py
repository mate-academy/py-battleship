class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.decks = self.calculate_decks(start, end)
        self.is_drowned = is_drowned

    @staticmethod
    def calculate_decks(start: tuple, end: tuple) -> list:
        decks = []
        if start[0] < end[0]:
            for cell in range(start[0], end[0] + 1):
                decks.append(Deck(cell, start[1]))
        elif start[1] < end[1]:
            for cell in range(start[1], end[1] + 1):
                decks.append(Deck(start[0], cell))
        else:
            decks.append(Deck(start[0], start[1]))

        return decks

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        for deck in self.decks:
            if deck.is_alive:
                return
        self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:

        self.field = self.create_ships(ships)

    @staticmethod
    def create_ships(ships: list) -> dict:
        field = {}
        for coordinates in ships:
            field[coordinates] = Ship(*coordinates)
        return field

    def fire(self, location: tuple) -> str:

        for ship in self.field.values():
            if ship.get_deck(location[0], location[1]):
                ship.fire(location[0], location[1])
                if ship.is_drowned:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"
