class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive
        pass


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.decks = []
        self.alive_decks = 0
        self.is_drowned = is_drowned
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column, is_alive=True))
                self.alive_decks += 1

    def get_deck(self, row: int, column: int) -> Deck:
        found_decks = [deck for deck in self.decks
                       if deck.row == row and deck.column == column]
        if len(found_decks) > 0:
            return found_decks[0]
        else:
            return None

    def deck_count(self) -> int:
        return len(self.decks)

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck is not None and deck.is_alive:
            deck.is_alive = False
            self.alive_decks -= 1
            self.is_drowned = self.alive_decks <= 0
            if self.is_drowned:
                return "Sunk!"
            else:
                return "Hit!"
        else:
            return "Miss!"


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.fields = {}
        self.ships = []
        for _tuple in ships:
            ship = Ship(_tuple[0], _tuple[1])
            for deck in ship.decks:
                self.fields[(deck.row, deck.column)] = ship
        self._validate_field()

    def fire(self, location: tuple) -> str:
        if location in self.fields.keys():
            return self.fields[location].fire(location[0], location[1])
        else:
            return "Miss!"

    def print_field(self) -> None:
        for row in range(0, 10):
            for column in range(0, 10):
                if (row, column) in self.fields.keys():
                    ship = self.fields[(row, column)]
                    if ship.is_drowned:
                        print("x")
                    elif not ship.get_deck(row, column).is_alive:
                        print("*")
                    else:
                        print(u"\u25A1")
                else:
                    print("~")
                print("  ")

    def _validate_field(self) -> bool:
        ships_by_decks = dict
        result = True
        for ship in self.ships:
            deck_count = ship.deck_count()
            ships_by_decks[deck_count] += 1
            for neighbour in self.ships:
                if ship != neighbour:
                    temp = Battleship._validate_ships_not_touch_one_another(
                        ship,
                        neighbour)
                    result = result and temp
                    if not result:
                        return False

        return (result and ships_by_decks[1] == 4
                and ships_by_decks[2] == 3
                and ships_by_decks[3] == 2
                and ships_by_decks[4] == 1)

    @classmethod
    def _validate_ships_not_touch_one_another(
            cls,
            ship1: Ship,
            ship2: Ship
    ) -> bool:
        result = Battleship._validate_ships_do_not_intersect(ship1, ship2)
        result = (result
                  and Battleship._validate_decks_do_not_touch(
                      ship1.decks[0],
                      ship2.decks[0]))
        result = (result
                  and Battleship._validate_decks_do_not_touch(
                      ship1.decks[-1],
                      ship2.decks[-1]))
        return result

    @classmethod
    def _validate_decks_do_not_touch(cls, deck1: Deck, deck2: Deck) -> bool:
        row_result = (deck1.row > deck2.row + 1
                      or deck1.row < deck2.row - 1)
        column_result = (deck1.column > deck2.column + 1
                         or deck1.column < deck2.column - 1)
        return row_result and column_result

    @classmethod
    def _validate_ships_do_not_intersect(
            cls,
            ship1: Ship,
            ship2: Ship
    ) -> bool:
        rows_not_intersect = (ship1.decks[0].row < ship2.decks[0].row
                              == ship1.decks[-1].row < ship2.decks[-1].row)
        rows_not_intersect = (rows_not_intersect
                              or (ship1.decks[0].row > ship2.decks[0].row
                                  == ship1.decks[-1].row
                                  > ship2.decks[-1].row))
        cols_not_intersect = (ship1.decks[0].column < ship2.decks[0].column
                              == (ship1.decks[-1].column
                                  < ship2.decks[-1].column))
        cols_not_intersect = (cols_not_intersect
                              or ((ship1.decks[0].column
                                   > ship2.decks[0].column)
                                  == (ship1.decks[-1].column
                                      > ship2.decks[-1].column)))
        return rows_not_intersect or cols_not_intersect
