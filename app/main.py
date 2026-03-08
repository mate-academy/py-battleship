class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple, end: tuple) -> None:
        self.decks = []
        self.is_drowned = False

        r1, c1 = start
        r2, c2 = end

        row_start, row_end = min(r1, r2), max(r1, r2)
        column_start, column_end = min(c1, c2), max(c1, c2)

        if r1 == r2:
            for column in range(column_start, column_end + 1):
                self.decks.append(Deck(r1, column))
        elif c1 == c2:
            for row in range(row_start, row_end + 1):
                self.decks.append(Deck(row, c1))

    def fire(self, row: int, column: int) -> None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False
                break

        self.is_drowned = all(not d.is_alive for d in self.decks)


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = [["~" for _ in range(10)] for _ in range(10)]
        self.ships_objects = []

        for start, end in ships:
            new_ship = Ship(start, end)
            self.ships_objects.append(new_ship)

            for deck in new_ship.decks:
                self.field[deck.row][deck.column] = "□"

    def fire(self, location: tuple) -> str:
        row, column = location

        if self.field[row][column] in ("~", "*", "X"):
            return "Miss!"

        for ship in self.ships_objects:
            if any(d.row == row and d.column == column for d in ship.decks):
                ship.fire(row, column)

                if ship.is_drowned:
                    for deck in ship.decks:
                        self.field[deck.row][deck.column] = "X"
                    return "Sunk!"

                self.field[row][column] = "*"
                return "Hit!"

        return "Miss!"

    def _validate_field(self) -> None:
        lengths = sorted([len(s.decks) for s in self.ships_objects])
        if lengths != [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]:
            raise ValueError("Invalid fleet composition")

        all_occupied = set()
        for ship in self.ships_objects:
            for deck in ship.decks:
                all_occupied.add((deck.row, deck.column))

        for ship in self.ships_objects:
            for deck in ship.decks:
                for dr in range(-1, 2):
                    for dc in range(-1, 2):
                        if dr == 0 and dc == 0:
                            continue
                        neighbor = (deck.row + dr, deck.column + dc)

                        if neighbor in all_occupied:
                            if not any(nd.row == neighbor[0]
                                       and nd.column == neighbor[1]
                                       for nd in ship.decks):
                                raise ValueError("Ships are too close")

    def print_field(self) -> None:
        for row in self.field:
            print(" ".join(row))
