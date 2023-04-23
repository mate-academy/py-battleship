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
                 start: tuple[int],
                 end: tuple[int],
                 is_drowned: bool = False) -> None:
        self.decks = [Deck(start[0], start[1])]
        if start[0] == end[0]:
            for i in range(start[1] + 1, end[1] + 1):
                self.decks.append(Deck(start[0], i))
        else:
            for i in range(start[0] + 1, end[0] + 1):
                self.decks.append(Deck(i, start[1]))
        self.is_drowned = is_drowned

    def get_deck(self,
                 row: int,
                 column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self,
             row: int,
             column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        for ship in ships:
            boat = Ship(ship[0], ship[1])
            for deck in boat.decks:
                self.field[(deck.row, deck.column)] = boat

    def fire(self, location: tuple) -> str:
        boat = self.field.get(location)
        if boat:
            boat.fire(location[0], location[1])
            if boat.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                boat = self.field.get((row, column))
                if boat:
                    if boat.is_drowned:
                        print("x", end="\t")
                    else:
                        if boat.get_deck(row, column).is_alive:
                            print(u"\u25A1", end="\t")
                        else:
                            print("*", end="\t")
                else:
                    print("~", end="\t")
            print()


if __name__ == "__main__":
    bshp = Battleship(
        ships=[
            ((2, 0), (2, 3)),
            ((4, 5), (4, 6)),
            ((3, 8), (3, 9)),
            ((6, 0), (8, 0)),
            ((6, 4), (6, 6)),
            ((6, 8), (6, 9)),
            ((9, 9), (9, 9)),
            ((9, 5), (9, 5)),
            ((9, 3), (9, 3)),
            ((9, 7), (9, 7)),
        ]
    )
    bshp.print_field()
