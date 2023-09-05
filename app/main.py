class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive
        self.is_ship_drowned = False

    def __repr__(self) -> str:
        if self.is_ship_drowned:
            return "  x  "
        if not self.is_alive:
            return "  *  "
        return u"  \u25A1  "


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.decks = []
        self.is_drowned = is_drowned
        self.exist = False
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.decks.append(
                    Deck(
                        row,
                        column
                    )
                )

    def __repr__(self) -> str:
        return "  ".join([str(deck) for deck in self.decks])

    def change_repr(self) -> None:
        for deck in self.decks:
            deck.is_ship_drowned = True

    def get_deck(self, row: int, column: int) -> Deck | str:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        # return f"There is not deck of this ship in ({row}, {column}) cell"

    def fire(self, row: int, column: int) -> None:
        alive_list = []

        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False
            alive_list.append(deck.is_alive)
        if not any(alive_list):
            self.is_drowned = True
            self.change_repr()


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        self.warships = []
        for ship in ships:

            start = ship[0]
            end = ship[1]
            warship = Ship(start, end)
            self.warships.append(warship)

            cur_row = start[0]

            for column in range(start[1], end[1] + 1):
                self.field[(cur_row, column)] = warship
                if cur_row != end[0]:
                    cur_row += 1

    def fire(self, location: tuple) -> str:
        if location in self.field:
            self.field[location].fire(location[0], location[1])
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        field = [["  ~  " for _ in range(10)] for _ in range(10)]

        for ship in self.field.values():
            if not ship.exist:
                for deck in ship.decks:
                    field[deck.row][deck.column] = str(deck)

        for row in field:
            print("".join(row))
