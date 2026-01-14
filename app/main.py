from __future__ import annotations


class Cell:
    def __init__(self, row: int, column: int, symbol: str = "~") -> None:
        self.row = row
        self.column = column
        self.symbol = symbol


class Deck(Cell):
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        super().__init__(row, column, "□")
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
        self.decks = self.create_decs(start, end)
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck:
        return [
            deck for deck in self.decks
            if deck.row == row and deck.column == column
        ][0]

    def fire(self, row: int, column: int) -> str:
        if self.is_drowned:
            return "The ship in this location already drowned"

        deck = self.get_deck(row, column)
        if deck.is_alive is False:
            return "The deck has already been struck"

        deck.is_alive = False
        deck.symbol = "*"
        return "Sunk!" if self.if_all_deck_is_damaged() else "Hit!"

    def if_all_deck_is_damaged(self) -> bool:
        if not any([deck.is_alive for deck in self.decks]):
            self.is_drowned = True
            for deck in self.decks:
                deck.symbol = "x"
            return True
        return False

    @staticmethod
    def create_decs(start: tuple, end: tuple) -> list[Deck]:
        list_of_decks = []
        if start[0] == end[0]:
            # ship located horizontally
            ship_length = end[1] - start[1] + 1
            for i in range(ship_length):
                list_of_decks.append(Deck(start[0], start[1] + i))
        else:
            # ship located vertically
            ship_length = end[0] - start[0] + 1
            for i in range(ship_length):
                list_of_decks.append(Deck(start[0] + i, start[1]))

        return list_of_decks

    @classmethod
    def create_ship(cls, ship_cords: tuple) -> Ship:
        return cls(*ship_cords)


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = self.create_empty_field()
        self.ships = ships

    @property
    def ships(self) -> list[Ship]:
        return self._ships

    @ships.setter
    def ships(self, ships: list[tuple]) -> None:
        self._ships = [Ship.create_ship(cords) for cords in ships]
        self.add_ships_to_the_field()

    def fire(self, location: tuple) -> str:
        try:
            if not isinstance(self.field[location], Ship):
                return "Miss!"
            result = self.field[location].fire(*location)
            # If you want to print field -> uncomment func() below
            # self.print_field()
            return result
        except (TypeError, KeyError):
            print(
                f"Location {location} isn't correct. "
                f"Must be in range (0-9, 0-9)"
            )

    def add_ships_to_the_field(self) -> None:
        for ship in self.ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def print_field(self) -> None:
        for i, (cords, cell) in enumerate(self.field.items()):
            if i % 10 == 0:
                print()
            print(self.get_symbol_from_cell(cords, cell), end="  ")
        print("")

    @staticmethod
    def get_symbol_from_cell(cords: tuple[int, int], cell: Cell | Ship) -> str:
        if isinstance(cell, Ship):
            return cell.get_deck(cords[0], cords[1]).symbol

        return cell.symbol

    @staticmethod
    def create_empty_field() -> dict[tuple[int, int], Cell]:
        return ({
            (i, j): Cell(i, j)
            for i in range(10)
            for j in range(10)
        })
