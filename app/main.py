class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self._create_decks()

    def _create_decks(self) -> list[Deck]:
        decks = []
        if self.start[0] == self.end[0]:  # Horizontal ship
            for col in range(self.start[1], self.end[1] + 1):
                decks.append(Deck(self.start[0], col))
        else:  # Vertical ship
            for row in range(self.start[0], self.end[0] + 1):
                decks.append(Deck(row, self.start[1]))
        return decks

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> bool:
        deck = self.get_deck(row, column)
        if deck and deck.is_alive:
            deck.is_alive = False
            self.is_drowned = all(not d.is_alive for d in self.decks)
            return True
        return False


class Battleship:
    def __init__(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        self.field = {}
        self.ships = []
        for ship_coords in ships:
            ship = Ship(*ship_coords)
            self.ships.append(ship)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple[int, int]) -> str:
        if location not in self.field:
            return "Miss!"
        ship = self.field[location]
        row, col = location
        hit = ship.fire(row, col)
        if not hit:
            return "Miss!"
        if ship.is_drowned:
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        field_visual = [["~" for _ in range(10)] for _ in range(10)]
        for (row, col), ship in self.field.items():
            deck = ship.get_deck(row, col)
            if deck.is_alive:
                field_visual[row][col] = "□"
            elif ship.is_drowned:
                field_visual[row][col] = "x"
            else:
                field_visual[row][col] = "*"
        for row in field_visual:
            print(" ".join(row))

    def _validate_field(self) -> bool:
        ship_counts = {1: 0, 2: 0, 3: 0, 4: 0}
        for ship in self.ships:
            length = len(ship.decks)
            if length in ship_counts:
                ship_counts[length] += 1
        return (
            ship_counts[1] == 4
            and ship_counts[2] == 3
            and ship_counts[3] == 2
            and ship_counts[4] == 1
        )
