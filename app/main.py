class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        self.decks = []
        if start[0] == end[0]:
            row = start[0]
            for col in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
                self.decks.append(Deck(row, col))

        elif start[1] == end[1]:
            col = start[1]
            for row in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
                self.decks.append(Deck(row, col))
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> bool | None:
        deck = self.get_deck(row, column)
        if deck is None:
            return None
        deck.is_alive = False
        if all(not d.is_alive for d in self.decks):
            self.is_drowned = True
        return True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = []
        for ship in ships:
            self.field.append(Ship(ship[0], ship[1]))
        self._validate_field()

    def fire(self, location: tuple) -> str:
        for ship in self.field:
            hit = ship.fire(location[0], location[1])
            if hit is not None:
                if ship.is_drowned:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for i in range(10):
            for jj in range(10):
                not_ship = 0
                for ship in self.field:
                    if ship.get_deck(i, jj) is not None:
                        not_ship += 1
                        if ship.is_drowned:
                            print("x", end=" ")
                            break
                        elif not ship.get_deck(i, jj).is_alive:
                            print("*", end=" ")
                            break
                        else:
                            print(u"\u25A1", end=" ")
                            break
                if not_ship == 0:
                    print("~", end=" ")
            print(" ")

    def _validate_field(self) -> None:
        if len(self.field) != 10:
            raise ValueError(f"Expected 10 ships, "
                             f"but found {len(self.field)}.")
        for i in range(1, 5):
            expected_count = 5 - i
            deck_ships = [ship for ship in self.field if len(ship.decks) == i]
            if len(deck_ships) != expected_count:
                raise ValueError(
                    f"Expected {expected_count} ship(s) of "
                    f"length {i}, but found {len(deck_ships)}.")
