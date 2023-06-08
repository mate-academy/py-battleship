from typing import Optional


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
        print("decks: ", self.decks)

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if (row, column) == deck.cell:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        self.is_drowned = not any([deck.is_alive for deck in self.decks])


class Battleship:

    def __init__(self, ships: list) -> None:
        self.field = {}
        for ship in ships:
            ship = Ship(ship[0], ship[1])
            for deck in ship.decks:
                self.field[deck.cell] = ship

        self._validate_field()

    def fire(self, location: tuple) -> str:
        if location in self.field:
            self.field[location].fire(location[0], location[1])
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def _validate_field(self) -> None:
        len_is_10 = len(self.field) == 20
        all_ships = []
        for ship in set(self.field.values()):
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
            raise Exception("You break the rules of battleship game")

    def __str__(self) -> str:
        field = []
        for _ in range(10):
            field.append(["~" for _ in range(10)])

        for ship in self.field.values():
            if ship.is_drowned:
                for deck in ship.decks:
                    x, y = deck.cell
                    field[x][y] = "x"
                continue
            for deck in ship.decks:
                x, y = deck.cell
                if deck.is_alive:
                    field[x][y] = "□"
                else:
                    field[x][y] = "*"

        new_field = ""
        for line in field:
            new_field += "      ".join(line) + "\n"

        return new_field
