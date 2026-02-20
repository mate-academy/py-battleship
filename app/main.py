class Deck:
    def __init__(
            self,
            row: int,
            column: int,
            is_alive: bool = True
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: int,
            end: int,
            is_drowned: bool = False
    ) -> None:
        start_x, start_y = start
        end_x, end_y = end
        self.is_drowned = is_drowned
        self.decks = []

        if start_x == end_x:
            for y_coord in range(
                    min(start_y, end_y),
                    max(start_y, end_y) + 1):
                self.decks.append(Deck(start_x, y_coord))

        elif start_y == end_y:
            for x_coord in range(
                    min(start_x, end_x),
                    max(start_x, end_x) + 1):
                self.decks.append(Deck(x_coord, start_y))
        else:
            raise ValueError

    def get_deck(
            self,
            row: int,
            column: int
    ) -> None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(
            self,
            row: int,
            column: int
    ) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            for _deck in self.decks:
                if _deck.is_alive is True:
                    return
            self.is_drowned = True


class Battleship:
    def __init__(
            self,
            ships: list
    ) -> None:
        self.ships = []
        self.field = {}
        for start, end in ships:
            new_ship = Ship(start, end)
            self.ships.append(new_ship)

        for ship in self.ships:
            for deck in ship.decks:
                coord = (deck.row, deck.column)
                self.field[coord] = ship

        self._validate_field()

    def print_field(self) -> None:
        for row in range(10):
            for colum in range(10):
                ship = self.field.get((row, colum))
                if ship:
                    deck = ship.get_deck(row, colum)
                    if ship.is_drowned:
                        print("x", end=" ")
                    elif not deck.is_alive:
                        print("*", end=" ")
                    else:
                        print("□", end=" ")
                else:
                    print("~", end=" ")
            print()

    def _validate_field(self) -> None:
        lengths = [len(s.decks) for s in self.ships]
        if (lengths.count(4) != 1 or lengths.count(3) != 2
                or lengths.count(2) != 3 or lengths.count(1) != 4):
            raise ValueError
        for ship in self.ships:
            for deck in ship.decks:
                for dr in range(-1, 2):
                    for dc in range(-1, 2):
                        if dr == 0 and dc == 0:
                            continue
                        neighbor_coord = (deck.row + dr, deck.column + dc)
                        neighbor_ship = self.field.get(neighbor_coord)

                        if neighbor_ship and neighbor_ship is not ship:
                            raise ValueError

    def fire(
            self,
            location: tuple
    ) -> str:
        if location not in self.field:
            return "Miss!"
        target_ship = self.field[location]
        target_ship.fire(*location)
        if target_ship.is_drowned:
            return "Sunk!"
        return "Hit!"
