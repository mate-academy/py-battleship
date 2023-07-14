from app.graphics import Surface


class Deck:
    def __init__(self, row: int, column: int) -> None:
        self.row = row
        self.column = column
        self.is_alive: bool = True
        self.texture = "□"

    def __bool__(self) -> bool:
        return self.is_alive


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned: bool = False
        self.decks: list[Deck] = self.generate_decks()

    def generate_decks(self) -> list[Deck]:
        decks = list()
        x0, y0 = self.start
        x1, y1 = self.end
        for row in range(y0, y1 + 1):
            for column in range(x0, x1 + 1):
                decks.append(Deck(row, column))
        return decks

    def get_deck(self, row: int, column: int) -> Deck | None:
        cords_list = [(deck.row, deck.column) for deck in self.decks]
        if (row, column) in cords_list:
            index = cords_list.index((row, column))
            return self.decks[index]

    def fire(self, column: int, row: int) -> str:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            deck.texture = "*"
            if not self:
                for deck in self.decks:
                    deck.texture = "x"
                self.is_drowned = True
                return "Sunk!"
            return "Hit!"

    def __bool__(self) -> bool:
        return any(bool(deck) for deck in self.decks)

    def __len__(self) -> int:
        return len(self.decks)


class Battleship:
    def __init__(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        self.ships: list[Ship] = self.generate_ships(ships)
        self.field: dict[tuple[int, int], Ship] = self.generate_field()

    @staticmethod
    def generate_ships(
            ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> list[Ship]:
        result = list()
        for start, end in ships:
            result.append(Ship(start, end))
        return result

    def generate_field(self) -> dict[tuple[int, int], Ship]:
        field = dict()
        for ship in self.ships:
            cords_list = [(deck.column, deck.row) for deck in ship.decks]
            for cords in cords_list:
                field[cords] = ship
        return field

    def fire(self, location: tuple[int, int]) -> str:
        if location in self.field:
            return self.field[location].fire(*location)
        return "Miss!"

    def print_field(self) -> None:
        surface = Surface(10, 10, "~")
        for cords in self.field:
            texture = self.field[cords].get_deck(*cords).texture
            column, row = cords
            surface.draw_point(row, column, texture)
        print(surface)

    def _validate_field(self) -> None:
        assert len(self.ships) == 10
        assert sorted(map(len, self.ships)) == [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
        for cords in self.field:
            for row in range(cords[1] - 1, cords[1] + 2):
                for column in range(cords[0] - 1, cords[0] + 2):
                    if (column, row) in self.field:
                        assert self.field[(column, row)] == self.field[cords]
