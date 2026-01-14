class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple,
                 end: tuple, is_drowned: bool = False) -> None:
        self.is_drowned = is_drowned
        self.cells = {(row, col) : Deck(row, col)
                      for row in range(start[0], end[0] + 1)
                      for col in range(start[1], end[1] + 1)}
        self.decks = list(self.cells.values())

    def get_deck(self, row: int, column: int) -> str:
        if self.is_drowned:
            return "X"
        elif cell := self.cells.get((row, column)):
            if cell.is_alive:
                return "□"
            else:
                return "*"

    def hit_deck(self) -> int:
        return sum(1 for deck in self.cells.values() if not deck.is_alive)

    def dimension(self) -> int:
        return len(self.cells)

    def fire(self, row: int, column: int) -> bool:
        self.cells.get((row, column)).is_alive = False
        if self.hit_deck() == self.dimension():
            self.is_drowned = True
        return self.is_drowned


class Battleship:
    def __init__(self, ships: dict) -> None:
        self.ships = [Ship(start, end) for start, end in ships]
        self.field = {(deck.row, deck.column): ship_obj
                      for ship_obj in self.ships
                      for deck in ship_obj.cells.values()}
        self._validate_field()

    def fire(self, location: tuple) -> None:
        if ship := self.field.get(location):
            if ship.fire(*location):
                return "Sunk!"
            else:
                return "Hit!"
        else:
            return "Miss!"

    def print_field(self) -> None:
        for row in range(0, 10):
            for col in range(0, 10):
                if ship := self.field.get((row, col)):
                    print(ship.get_deck(row, col), end="")
                else:
                    print("~", end="")
            print("")
        print("\n")

    @staticmethod
    def is_touch(cell: tuple, other_cell: tuple) -> bool:
        return (other_cell[0] in range(cell[0] - 1, cell[0] + 2)
                and other_cell[1] in range(cell[1] - 1, cell[1] + 2))

    def _validate_field(self) -> None:
        if (len(self.ships)) != 10:
            raise ValueError("Must be: 10 Ships !")

        ship_list = list(ship.dimension() for ship in self.ships)
        if ({x : ship_list.count(x) for x in set(ship_list)}
                != {1: 4, 2: 3, 3: 2, 4: 1}):
            raise ValueError("Must be: 4 one-deck, "
                             "3 two-deck, "
                             "2 three-deck, "
                             "1 four-deck Ships !")

        for (cell, ship) in self.field.items():
            for (other_cell, other_ship) in self.field.items():
                if ship == other_ship:
                    break
                if self.is_touch(cell, other_cell):
                    raise ValueError(f"Ships must not be touched each other ! "
                                     f"Check: {cell} with {other_cell}")
                    pass
        return
