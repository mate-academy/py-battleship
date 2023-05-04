class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.cell = (row, column)
        self.is_alive = is_alive


class Ship:

    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:

        self.decks = []
        for row_index in range(start[0], end[0] + 1):
            for column_index in range(start[1], end[1] + 1):
                self.decks.append(Deck(row_index, column_index))
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> tuple:
        for _deck in self.decks:
            if (row, column) in _deck.cell:
                return _deck.cell

    def fire(self, row: int, column: int) -> None:
        if (row, column) in self.decks:
            if not self.decks:
                self.is_drowned = True


class Battleship:

    def __init__(self, ships: list) -> None:
        self.field = {}
        for _ship in ships:
            self.field[_ship] = Ship(_ship[0], _ship[1])

        self._validate_field()

    def fire(self, location: tuple) -> str:
        for _ship in self.field.values():
            for _deck in _ship.decks:
                if _deck.cell == location:
                    _deck.is_alive = False
                    are_any_alive = [_deck.is_alive for _deck in _ship.decks]
                    if not any(are_any_alive):
                        _ship.is_drowned = True
                        return "Sunk!"
                    _deck.is_alive = False
                    return "Hit!"
        return "Miss!"

    def _validate_field(self) -> None:
        len_is_10 = len(self.field) == 10
        all_ships = []
        for _ship in self.field.values():
            all_ships.append(len(_ship.decks))

        one_four_deck = all_ships.count(4) == 1
        two_triple_deck = all_ships.count(3) == 2
        three_double_deck = all_ships.count(2) == 3
        four_single_deck = all_ships.count(1) == 4

        if all((
                len_is_10,
                one_four_deck,
                two_triple_deck,
                three_double_deck,
                four_single_deck
        )):
            print("Field is validated")
        else:
            print("You break the rules of battleship game")

    def _print(self) -> None:
        field = []
        for _ in range(10):
            field.append(["~" for _ in range(10)])

        for _, ship in self.field.items():
            if ship.is_drowned:
                for deck in ship.decks:
                    field[deck.cell[0]][deck.cell[1]] = "x"
            else:
                for deck in ship.decks:
                    if deck.is_alive:
                        field[deck.cell[0]][deck.cell[1]] = "□"
                    else:
                        field[deck.cell[0]][deck.cell[1]] = "*"
        for line in field:
            print("      ".join(line))
