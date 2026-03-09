class Deck:
    def __init__(
            self,
            row: tuple,
            column: tuple,
            is_alive: bool = True
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned
        self.decks = []
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                deck = Deck(row, column)
                self.decks.append(deck)

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: tuple, column: tuple) -> str:
        deck = self.get_deck(row, column)

        if deck:
            deck.is_alive = False

            if all(not deck.is_alive for deck in self.decks):
                self.is_drowned = True
                return "Sunk!"

        return "Hit!"


class Battleship:
    def __init__(self, ships: list[Ship]) -> None:
        self.ships = []
        self.field = {}
        for start, end in ships:
            ship = Ship(start, end)
            self.ships.append(Ship)

            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

        self.game_desk = [["~" for _ in range(10)] for _ in range(10)]
        for row, column in self.field.keys():
            self.game_desk[row][column] = u"\u25A1"

    def _validate_field(self) -> None:
        assert len(self.ships) == 10

        counts = {1: 0, 2: 0, 3: 0, 4: 0}
        for ship in self.ships:
            deck_count = len(ship.decks)
            assert deck_count in counts
            counts[deck_count] += 1

        assert counts[1] == 4
        assert counts[2] == 3
        assert counts[3] == 2
        assert counts[4] == 1

        occupied = set()
        for ship in self.ships:
            for deck in ship.decks:
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        neighbor = (deck.row + dr, deck.column + dc)
                        if neighbor in occupied:
                            raise AssertionError
                occupied.add((deck.row, deck.column))

    def fire(self, location: tuple) -> str:
        game_desk = self.game_desk
        if location not in self.field:
            game_desk[location[0]][location[1]] = "*"
            return "Miss!"

        ship = self.field[location]
        hit = ship.fire(location[0], location[1])
        if hit == "Hit!" or hit == "Sunk!":
            game_desk[location[0]][location[1]] = "X"
        return hit

    def print_field(self) -> None:
        for desk in self.game_desk:
            print(" ".join(desk))
