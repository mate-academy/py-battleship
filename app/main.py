class Deck:
    def __init__(
            self, row: int, column: int, is_alive: bool = True
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self, start: tuple, end: tuple, is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned
        self.decks = list()
        if start[0] < end[0]:
            self.decks.extend([
                Deck(deck_n, start[1])
                for deck_n in range(start[0], end[0] + 1)
            ])
        elif start[1] < end[1]:
            self.decks.extend([
                Deck(start[0], deck_n)
                for deck_n in range(start[1], end[1] + 1)
            ])
        else:
            self.decks.append(Deck(start[0], start[1]))

        self.health = len(self.decks)

    def get_deck(self, row: int, column: int) -> Deck:
        if result := [
            deck
            for deck in self.decks
            if deck.row == row and deck.column == column
        ][0]:
            return result
        else:
            raise IndexError

    def fire(self, row: int, column: int) -> None:
        if deck := self.get_deck(row, column):
            deck.is_alive = False
            self.health -= 1
        if self.health == 0:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple, tuple]) -> None:
        self.field = dict()
        for start_stop in ships:
            new_ship = Ship(start_stop[0], start_stop[1])
            for deck in new_ship.decks:
                self.field[deck.row, deck.column] = new_ship

    def fire(self, location: tuple[int, int]) -> str:
        if location not in self.field:
            return "Miss!"

        self.field[location].fire(location[0], location[1])
        if self.field[location].health == 0:
            return "Sunk!"
        else:
            return "Hit!"

    def field_print(self) -> None:
        for row in range(10):
            for column in range(10):
                if (row, column) in self.field:
                    print(u"\u25A1", 5 * " ", end="")
                else:
                    print("~", 5 * " ", end="")
            print()
