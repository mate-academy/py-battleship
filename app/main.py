class Deck:
    def __init__(
            self,
            row: int,
            column: int,
            is_alive: bool = True) -> None:
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
        if start[0] == end[0]:
            self.decks = [
                Deck(start[0], coord)
                for coord in range(start[1], end[1] + 1)
            ]
        else:
            self.decks = [
                Deck(coord, start[1])
                for coord in range(start[0], end[0] + 1)
            ]

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        if not any(deck.is_alive for deck in self.decks):
            self.is_drowned = True
            return "Sunk!"
        return "Hit!"


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        self.ships = ships

        for ship_coords in ships:
            new_ship = Ship(ship_coords[0], ship_coords[1])
            self.field[
                tuple((deck.row, deck.column)
                      for deck in new_ship.decks)
            ] = new_ship
        self._validate_field()

    def fire(self, location: tuple) -> str:
        for ship_decks, ship in self.field.items():
            if location in ship_decks:
                return ship.fire(location[0], location[1])
        return "Miss!"

    def print_field(self) -> None:
        battleship_field = []
        for row in range(10):
            battleship_field.append(["~"] * 10)

        for ship_decks, ship in self.field.items():
            if ship.is_drowned:
                for deck in ship_decks:
                    battleship_field[deck[0]][deck[1]] = "x"
            else:
                for deck in ship.decks:
                    if deck.is_alive:
                        battleship_field[deck.row][deck.column] = u"\u25A1"
                    else:
                        battleship_field[deck.row][deck.column] = "*"

        for row in battleship_field:
            print("    ".join(row))

    def _validate_field(self) -> None:
        assert len(self.ships) == 10
        assert [len(ship) for ship in sorted(self.field, key=len)] == [
            1, 1, 1, 1, 2, 2, 2, 3, 3, 4
        ]

        for index in range(len(self.field)):
            field_lst = list(self.field.copy())
            current_elem = field_lst.pop(index)
            coords_list = [i for x in field_lst for i in x]
            for el in current_elem:
                assert any([
                    (el[0] + 1, el[1] + 1) in coords_list,
                    (el[0] - 1, el[1] - 1) in coords_list,
                    (el[0] - 1, el[1] + 1) in coords_list,
                    (el[0] + 1, el[1] - 1) in coords_list,
                    (el[0] + 1, el[1]) in coords_list,
                    (el[0] - 1, el[1]) in coords_list,
                    (el[0], el[1] + 1) in coords_list,
                    (el[0], el[1] - 1) in coords_list,
                ]) is False
