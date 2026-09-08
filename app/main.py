class Deck:
    def __init__(self,
                 row: int,
                 column: int,
                 is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def get_is_alive(self) -> bool:
        return self.is_alive

    def __repr__(self) -> str:
        return f"Deck({self.row}, {self.column}), {self.is_alive}"


class Ship:
    def __init__(self,
                 start: tuple[int, int],
                 end: tuple[int, int],
                 is_drowned: bool = False) -> None:
        self.decks = self.create_decks_list(start, end)
        self.is_drowned = is_drowned

    def get_deck(self,
                 row: int,
                 column: int) -> Deck | None:
        return next(
            (deck for deck in self.decks
             if deck.row == row and deck.column == column)
            , None)

    def check_is_drowned(self) -> bool:
        return all(deck.is_alive is False for deck in self.decks)

    def fire(self,
             row: int,
             column: int) -> str:
        deck = self.get_deck(row, column)
        message = "Miss!"
        if deck:
            deck.is_alive = False
            message = "Hit!"
            if self.check_is_drowned():
                self.is_drowned = True
                message = "Sunk!"

        return message

    @staticmethod
    def create_decks_list(start: tuple[int, int],
                          end: tuple[int, int]) -> list[Deck]:
        moving_index = 1 if start[0] == end[0] else 0
        decks = []

        for range_index in range(start[moving_index], end[moving_index] + 1):

            if moving_index == 0:
                decks.append(Deck(range_index, start[1]))
            else:
                decks.append(Deck(start[0], range_index))

        return decks


class Battleship:
    def __init__(self,
                 ships: list[tuple[tuple[int, int], tuple[int, int]]]) -> None:
        self.field = self.map_cells_to_ships(ships)

    def fire(self,
             location: tuple) -> str:
        ship = self.field.get(location, None)
        if ship:
            return ship.fire(location[0], location[1])
        return "Miss!"

    def print_field(self) -> None:
        for x_loc in range(10):
            row = []
            for y_loc in range(10):

                cell_symbol = self.field.get((x_loc, y_loc), "~")

                if isinstance(cell_symbol, Ship):
                    cell_symbol = u"\u25A1" \
                        if cell_symbol.get_deck(x_loc, y_loc).get_is_alive() \
                        else u"\u25EA"

                row.append(cell_symbol)
            print(" ".join(row))
            row.clear()

    @staticmethod
    def map_cells_to_ships(
            ships_coordinates: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> dict[tuple[int, int], Ship]:
        ships = [Ship(coordinate[0], coordinate[1])
                 for coordinate in ships_coordinates]

        return {
            (deck.row, deck.column): ship
            for ship in ships
            for deck in ship.decks
        }
