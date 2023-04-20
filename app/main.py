class Deck:
    def __init__(self,
                 row: int,
                 column: int,
                 is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        self.decks = [Deck(start[0], start[1])]
        step = end[0] - start[0] + end[1] - start[1]
        for i in range(1, step + 1):
            if end[0] == start[0]:
                self.decks.append(Deck(start[0], start[1] + i))
            else:
                self.decks.append(Deck(start[0] + i, start[1]))
        self.is_drowned = is_drowned

    def get_deck(self,
                 row: int,
                 column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self,
             row: int,
             column: int) -> None:
        self.get_deck(row, column).is_alive = False
        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self,
                 ships: list) -> None:
        self.field = {}
        for ship in ships:
            boat = Ship(ship[0], ship[1])
            self.field[ship[0]] = boat
            step = ship[1][0] - ship[0][0] + ship[1][1] - ship[0][1]
            for i in range(1, step + 1):
                if ship[0][0] == ship[1][0]:
                    self.field[(ship[0][0], ship[0][1] + i)] = boat
                else:
                    self.field[(ship[0][0] + i, ship[0][1])] = boat

    def fire(self,
             location: tuple) -> str:
        if location not in self.field:
            return "Miss!"
        self.field[location].fire(location[0], location[1])
        if self.field[location].is_drowned:
            return "Sunk!"
        return "Hit!"
