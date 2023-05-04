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
        if start[0] == end[0]:
            for i in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], i))
        else:
            for i in range(start[0], end[0] + 1):
                self.decks.append(Deck(i, end[1]))
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> tuple:
        for deck in self.decks:
            if (row, column) in deck.cell:
                return deck.cell

    def fire(self, row: int, column: int) -> None:
        if (row, column) in self.decks:
            if not self.decks:
                self.is_drowned = True


class Battleship:

    def __init__(self, ships: list) -> None:
        self.field = {}
        self.battle_field = []
        for _ in range(10):
            self.battle_field.append(["~" for _ in range(10)])

        for ship in ships:
            self.field[ship] = Ship(ship[0], ship[1])
            for deck in self.field[ship].decks:
                self.battle_field[deck.cell[0]][deck.cell[1]] = "□"
        self._validate_field()

    def fire(self, location: tuple) -> str:
        for ship in self.field.values():
            for deck in ship.decks:
                if deck.cell == location:
                    x, y = deck.cell
                    deck.is_alive = False
                    are_any_alive = [deck.is_alive for deck in ship.decks]
                    if not any(are_any_alive):
                        ship.is_drowned = True
                        for deck in ship.decks:
                            x, y = deck.cell
                            self.battle_field[x][y] = "x"
                        return "Sunk!"
                    self.battle_field[x][y] = "*"
                    return "Hit!"
        return "Miss!"

    def _validate_field(self) -> None:
        len_is_10 = len(self.field) == 10
        all_ships = []
        for ship in self.field.values():
            all_ships.append(len(ship.decks))

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

    def print_field(self) -> None:
        for row in self.battle_field:
            print("       ".join(row))
