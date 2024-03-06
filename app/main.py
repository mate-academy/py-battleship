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
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        if start == end:
            self.decks = [Deck(start[0], start[1])]
        if start[0] == end[0]:
            self.decks = [Deck(start[0], start[1] + i)
                          for i in range(abs(start[1] - end[1]) + 1)]
        if start[1] == end[1]:
            self.decks = [Deck(start[0] + i, end[1])
                          for i in range(abs(start[0] - end[0]) + 1)]

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> int:
        attacked_deck = self.get_deck(row, column)
        attacked_deck.is_alive = False
        if all(deck.is_alive for deck in self.decks):
            self.is_drowned = True
        return sum(deck.is_alive for deck in self.decks)


class Battleship:

    def __init__(self, ships: list[tuple[tuple, tuple]]) -> None:
        self.field = {}
        if ships is not None:
            for coordinates_ship in ships:
                ship = Ship(coordinates_ship[0], coordinates_ship[1])
                for deck in ship.decks:
                    self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple[int, int]) -> str:
        if location not in self.field:
            self.field[location] = "Miss!"
            return "Miss!"
        elif isinstance(self.field[location], Ship):
            ship = self.field[location]
            fire = ship.fire(location[0], location[1])
            if ship.is_drowned:
                return "Drowned!"
            if fire == 0:
                return "Sunk!"
            return "Hit!"

    def print_field(self) -> None:
        game_field = [["\U0001F7E6"] * 10 for _ in range(10)]
        for ceil in self.field:
            if self.field[ceil] == "Miss!":
                game_field[ceil[0]][ceil[1]] = "\u274C"
            else:
                deck = self.field[ceil].get_deck(ceil[0], ceil[1])
                if deck.is_alive:
                    game_field[ceil[0]][ceil[1]] = "\u26F5"
                else:
                    game_field[ceil[0]][ceil[1]] = "\U0001F4A5"
        for row in game_field:
            print(*row)
        print("-" * 32)
