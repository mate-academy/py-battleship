from typing import List, Tuple, Dict


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
        start: Tuple[int, int],
        end: Tuple[int, int],
        is_drowned: bool = False
    ) -> None:
        self.decks = []
        self.is_drowned = is_drowned

        r1, c1 = start
        r2, c2 = end

        # горизонтальный корабль
        if r1 == r2:
            for _c in range(min(c1, c2), max(c1, c2) + 1):
                self.decks.append(Deck(r1, _c))

        # вертикальный корабль
        elif c1 == c2:
            for _r in range(min(r1, r2), max(r1, r2) + 1):
                self.decks.append(Deck(_r, c1))
        else:
            raise ValueError("Корабль должен быть прямой линией")

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)

        if deck and deck.is_alive:
            deck.is_alive = False

        # проверяем, утонул ли корабль
        if all(not d.is_alive for d in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(
        self,
        ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        self.field: Dict[Tuple[int, int], Ship] = {}  # (row, col) -> Ship

        for start, end in ships:
            ship = Ship(start, end)

            for deck in ship.decks:
                coord = (deck.row, deck.column)

                if coord in self.field:
                    raise ValueError("Пересечение кораблей")

                self.field[coord] = ship

    def fire(self, location: tuple) -> str:
        row, col = location

        # промах
        if location not in self.field:
            return "Miss!"

        ship = self.field[location]
        deck = ship.get_deck(row, col)

        # если уже стреляли
        if not deck.is_alive:
            return "Miss!"

        ship.fire(row, col)

        if ship.is_drowned:
            return "Sunk!"

        return "Hit!"
