class Deck:
    def __init__(self, row, column, is_alive=True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start, end, is_drowned=False) -> None:
        self.decks = []
        self.is_drowned = is_drowned

        if start[0] == end[0]:
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], column))

        elif start[1] == end[1]:
            for row in range(start[0], end[0] + 1):
                self.decks.append(Deck(row, start[1]))

    def get_deck(self, row, column) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row, column) -> str:
        self.get_deck(row, column).is_alive = False
        if all([not deck.is_alive for deck in self.decks]):
            self.is_drowned = True
            return "Sunk!"
        return "Hit!"


class Battleship:
    def __init__(self, ships) -> None:
        self.field = {}
        for ship in ships:
            ship_instance = Ship(*ship)
            for deck in ship_instance.decks:
                self.field[(deck.row, deck.column)] = ship_instance

    def fire(self, location: tuple) -> str:
        if location in self.field.keys():
            ship = self.field[location]
            return ship.fire(*location)
        return "Miss!"

