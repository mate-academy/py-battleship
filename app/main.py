class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple[int, int], end: tuple[int, int],
            is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []

        if start[0] == end[0]:
            for i in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], i))
        elif start[1] == end[1]:
            for i in range(start[0], end[0] + 1):
                self.decks.append(Deck(i, start[1]))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        return self.get_status()

    def get_status(self) -> str:
        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True
            return "Sunk!"
        return "Hit!"


class Battleship:
    def __init__(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        self.ships = [Ship(start, end) for start, end in ships]
        self.field = {}
        self._validate_field()

        for ship in self.ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple[int, int]) -> str:
        if location in self.field:
            return self.field[location].fire(location[0], location[1])
        return "Miss!"

    def _validate_field(self) -> None:
        ships = self.ships
        if len(ships) != 10:
            raise ValueError("Must be 10 ships")

        ship_counts = {1: 0, 2: 0, 3: 0, 4: 0}
        for ship in ships:
            ship_length = len(ship.decks)
            if ship_length in ship_counts:
                ship_counts[ship_length] += 1

        if ship_counts[1] != 4:
            raise ValueError("Must be 4 one-deck ships")
        if ship_counts[2] != 3:
            raise ValueError("Must be 3 two-deck ships")
        if ship_counts[3] != 2:
            raise ValueError("Must be 2 three-deck ships")
        if ship_counts[4] != 1:
            raise ValueError("Must be 1 four-deck ships")

        occupied_cells = set()
        for ship in self.ships:
            ship_cells = set()
            for deck in ship.decks:
                for d_row in range(-1, 2):
                    for d_col in range(-1, 2):
                        if d_row == 0 and d_col == 0:
                            continue
                        neighbor = (deck.row + d_row, deck.column + d_col)
                        if neighbor in occupied_cells:
                            raise ValueError("Ships should not be adjacent.")
                ship_cells.add((deck.row, deck.column))
            occupied_cells.update(ship_cells)

    def print_field(self) -> None:
        game_field = [["~"] * 10 for _ in range(10)]

        for (row, col), ship in self.field.items():
            deck = ship.get_deck(row, col)

            if ship.is_drowned:
                game_field[row][col] = "x"
            if not deck.is_alive:
                game_field[row][col] = "*"
            if deck.is_alive:
                game_field[row][col] = "□"

        for row in game_field:
            print("  ".join(row))
