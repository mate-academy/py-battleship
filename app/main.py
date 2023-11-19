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
            start: int,
            end: int,
            is_drowned: bool = False
    ) -> None:
        self.decks = [Deck(row, col)
                      for row, col in self.get_coordinates(start, end)]
        self.is_drowned = is_drowned

    @classmethod
    def get_coordinates(
            cls,
            start: tuple,
            end: tuple
    ) -> list[tuple]:
        return [(start[0] + i, start[1] + j)
                for i in range(end[0] - start[0] + 1)
                for j in range(end[1] - start[1] + 1)]

    def get_deck(
            self,
            row: int,
            column: int
    ) -> Deck | None:
        return next((deck for deck in self.decks if deck.row
                     == row and deck.column == column), None)

    def fire(
            self,
            row: int,
            column: int
    ) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if all(not deck_.is_alive for deck_ in self.decks):
                self.is_drowned = True


class Battleship:
    def __init__(
            self,
            ships: list
    ) -> None:
        self.field = {}
        for ship_start, ship_end in ships:
            ship = Ship(ship_start, ship_end)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(
            self,
            location: tuple
    ) -> str:
        if location not in self.field:
            return "Miss!"

        ship = self.field[location]
        deck = ship.get_deck(*location)

        if deck.is_alive:
            ship.fire(location[0], location[1])
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for col in range(10):
                location = (row, col)
                if location in self.field:
                    ship = self.field[location]
                    deck = ship.get_deck(row, col)
                    if deck.is_alive:
                        print(u"\u25A1", end=" ")
                    elif ship.is_drowned:
                        print("x", end=" ")
                    else:
                        print("*", end=" ")
                else:
                    print("~", end=" ")
            print()
