class Deck:
    def __init__(self, row: int, column: int , is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start, end, is_drowned=False):
        self.decks = [Deck(deck[0], deck[1], True) for deck in get_coordinates((start, end))]
        self.is_drowned = is_drowned


    def get_deck(self, row, column):
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

        return None


    def fire(self, row, column):
        deck = self.get_deck(row, column)
        deck.is_alive = False

        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships):
        self.field = {
            cell: ship_obj
            for ship in ships
            for ship_obj in [Ship(ship[0], ship[1], False)]
            for cell in get_coordinates(ship)
        }

    def fire(self, location: tuple):
        if location in self.field:
            ship = self.field.get(location)
            ship.fire(*location)
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"

        return "Miss!"


def get_coordinates(ship):
    size = abs(sum(ship[1]) - sum(ship[0])) + 1

    iterable_order = "y"

    if ship[0][0] != ship[1][0]:
        iterable_order = "x"

    start_coordinates = list(ship[0])
    coordinates = [tuple(start_coordinates)]

    for i in range(size - 1):
        if iterable_order == "x":
            start_coordinates[0] += 1
        else:
            start_coordinates[1] += 1
        coordinates.append(tuple(start_coordinates))

    return coordinates
