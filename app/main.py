class Deck:
    def __init__(
            self, row: int,
            column: int,
            is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return f"Deck({self.row}, {self.column}, {self.is_alive})"


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False) -> None:
        self.decks = []
        self.is_drowned = is_drowned
        self.start = start
        self.end = end

        self.deck_list_init()

    def deck_list_init(
            self) -> None:
        end_x, end_y = self.end
        start_x, start_y = self.start
        x_diagonal = abs(end_x - start_x)
        if x_diagonal:
            for deck in range(start_x, end_x + 1):
                self.decks.append(Deck(deck, start_y))
        else:
            for deck in range(start_y, end_y + 1):
                self.decks.append(Deck(start_x, deck))

    def get_deck(self, row: int, column: int) -> Deck | None:
        try:
            for deck in self.decks:
                if (row, column) == (deck.row, deck.column):
                    return deck
        except ValueError:
            return None

    def fire(self, row: int, column: int) -> None:
        fired_deck = self.get_deck(row, column)
        if fired_deck:
            fired_deck.is_alive = False
            self.ship_drowned()

    def ship_drowned(self) -> None:
        dead_counter = 0
        for deck in self.decks:
            if not deck.is_alive:
                dead_counter += 1
        if dead_counter == len(self.decks):
            self.is_drowned = True

    def __str__(self) -> str:
        return f"{str(self.decks)}, Drowned: {str(self.is_drowned)}"

    def __repr__(self) -> str:
        return f"Ship: {str(self.decks)}, Drowned: {str(self.is_drowned)}"


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        for ship_item in ships:
            start, end = ship_item
            ship_to_add = Ship(start, end)
            for cell in ship_to_add.decks:
                self.field[(cell.row, cell.column)] = ship_to_add

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            ship.fire(location[0], location[1])
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        battle_field = []
        for i in range(10):
            row = []
            for col in range(10):
                if (i, col) in self.field:
                    if not self.field[(i, col)].get_deck(i, col).is_alive:
                        row.append("x")
                    else:
                        row.append("□")
                else:
                    row.append("~")
            battle_field.append(row)

        for row in range(10):
            for column in range(10):
                print(battle_field[row][column], end=" ")
            print()
