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
        self.deck_list_init(start, end)

    def deck_list_init(
            self,
            start: tuple,
            end: tuple) -> None:
        end_x, end_y = end
        start_x, start_y = start
        x_diagonal = abs(end_x - start_x)
        if x_diagonal:
            for deck in range(start_x, end_x + 1):
                self.decks.append(Deck(deck, start_y))
        else:
            for deck in range(start_y, end_y + 1):
                self.decks.append(Deck(start_x, deck))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if (row, column) == (deck.row, deck.column):
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        fired_deck = self.get_deck(row, column)
        if fired_deck:
            fired_deck.is_alive = False
            if all(not deck.is_alive for deck in self.decks):
                self.is_drowned = True

    def __str__(self) -> str:
        return f"{str(self.decks)}, Drowned: {str(self.is_drowned)}"

    def __repr__(self) -> str:
        return f"Ship: {str(self.decks)}, Drowned: {str(self.is_drowned)}"

    def __len__(self) -> int:
        return len(self.decks)


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        list_of_ships = {}
        for ship_item in ships:
            start, end = ship_item
            ship_to_add = Ship(start, end)
            list_of_ships[ship_to_add] = len(ship_to_add)
            for cell in ship_to_add.decks:
                self.field[(cell.row, cell.column)] = ship_to_add

        self._validate_field(list_of_ships)

    def _validate_field(self, ships: dict) -> None:
        if len(ships) != 10:
            raise ValueError("Invalid amount of ships")

        amount_of_types = {1: 4, 2: 3, 3: 2, 4: 1}
        for amount, decks in amount_of_types.items():
            counter = 0
            for ship in ships:
                if decks == len(ship):
                    counter += 1
            if counter != amount:
                raise ValueError("Invalid fleet composition!")

        occupied_cells = set(self.field.keys())
        for (row, col) in occupied_cells:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    neighbor = (row + dr, col + dc)
                    if neighbor in occupied_cells:
                        if self.field[neighbor] != self.field[(row, col)]:
                            raise ValueError("Ships are touching!")

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            ship.fire(location[0], location[1])
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            row_str = ""
            for col in range(10):
                if (row, col) in self.field:
                    ship = self.field[(row, col)]
                    deck = next(d for d in ship.decks
                                if d.row == row and d.column == col)
                    if ship.is_drowned:
                        row_str += "x "
                    elif not deck.is_alive:
                        row_str += "* "
                    else:
                        row_str += "□ "
                else:
                    row_str += "~ "
            print(row_str)
