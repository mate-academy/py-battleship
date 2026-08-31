class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.coor = (row, column)
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.decks = []
        self.is_drowned = is_drowned
        if start == end:
            self.decks.append(Deck(*start))
        else:
            if start[0] == end[0]:
                for deck in range(start[1], end[1] + 1):
                    self.decks.append(Deck(start[0], deck))
            elif start[1] == end[1]:
                for deck in range(start[0], end[0] + 1):
                    self.decks.append(Deck(start[1], deck))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.coor == (row, column):
                return deck

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        if not any(deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        for ship in ships:
            ship = Ship(*ship)
            for deck in ship.decks:
                self.field[deck.coor] = ship

    def fire(self, location: tuple) -> str:
        ship = self.field.get(location)
        if ship is None:
            return "Miss!"
        ship.fire(*location)
        if ship.is_drowned:
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        field = [["~"] * 10 for _ in range(10)]
        for ship in set(self.field.values()):
            for deck in ship.decks:
                row, column = deck.coor
                if ship.is_drowned:
                    field[row][column] = "x"
                elif deck.is_alive:
                    field[row][column] = "□"
                else:
                    field[row][column] = "*"
        for res in field:
            print("".join(res))

    def _validate(self) -> None:
        ships = set(self.field.values())
        ships_var = [len(ship.decks) for ship in ships]
        if len(ships) != 10:
            print(f"There should "
                  f"be 10 ships. Currently: {len(ships)}")
        if ships_var.count(1) != 4:
            print(f"There should be 4 "
                  f"single-deck ships. Currently: {ships_var.count(1)}")
        if ships_var.count(2) != 3:
            print(f"There should be 4 "
                  f"double-deck ships. Currently: {ships_var.count(2)}")
        if ships_var.count(3) != 2:
            print(f"There should be 2 "
                  f"three-deck ships. Currently: {ships_var.count(3)}")
        if ships_var.count(4) != 1:
            print(f"There should be 1 "
                  f"four-deck ships. Currently: {ships_var.count(4)}")
