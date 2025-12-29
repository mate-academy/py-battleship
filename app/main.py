class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return f"Deck({self.row}, {self.column}, {self.is_alive})"


class Ship:
    def __init__(self, start: tuple, end: tuple) -> None:
        self.start = start
        self.end = end
        self.is_drowned = False  # За замовчуванням це завжди False
        self.decks = []
        if start[0] == end[0]:
            row = start[0]
            for col in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
                self.decks.append(Deck(row, col))
        elif start[1] == end[1]:
            col = start[1]
            for row in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
                self.decks.append(Deck(row, col))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if all(not deck.is_alive for deck in self.decks):
                self.is_drowned = True
                return "Sunk!"
            return "Hit!"
        return "Miss!"


class Battleship:
    def __init__(self,
                 ships: list[tuple[tuple[int, int], tuple[int, int]]]) -> None:
        self.ships = []
        self.field = {}

        # Створюємо кораблі з переданих кортежів координат
        for start, end in ships:
            ship = Ship(start, end)  # Створюємо об'єкт Ship з кожного кортежа
            self.ships.append(ship)
            for deck in ship.decks:
                self.field[(
                    deck.row, deck.column)] = ship  # Додаємо палуби в поле

    def fire(self, location: tuple[int, int]) -> str:
        row, col = location
        if (row, col) in self.field:
            ship = self.field[(row, col)]
            result = ship.fire(row, col)
            return result
        else:
            return "Miss!"
