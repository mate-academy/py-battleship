class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: int, end: int, is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        if self.end[0] > self.start[0]:
            self.decks = [
                Deck(i + self.start[0], self.start[1])
                for i in range(self.end[0] - self.start[0] + 1)
            ]
            self.is_columned_ship = False
        else:
            self.decks = [
                Deck(self.start[0], i + self.start[1])
                for i in range(self.end[1] - self.start[1] + 1)
            ]
            self.is_columned_ship = True

    def get_deck(self, row: int, column: int) -> None | Deck:
        if self.is_columned_ship and row != self.decks[0].row:
            return None

        if not self.is_columned_ship and column != self.decks[0].column:
            return None

        if (self.is_columned_ship
                and self.decks[0].column <= column <= self.decks[-1].column):
            return self.decks[column - self.decks[0].column]

        if (not self.is_columned_ship
                and self.decks[0].row <= row <= self.decks[-1].row):
            return self.decks[row - self.decks[0].row]

        return None

    def is_last_deck(self) -> int:
        return len([True for deck in self.decks if deck.is_alive]) == 1

    def fire(self, row: int, column: int) -> None:
        deck_to_destroy = self.get_deck(row, column)
        if deck_to_destroy:
            deck_to_destroy.is_alive = False

            if not any(deck.is_alive for deck in self.decks):
                self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = ships
        self.field = {}
        if not self._validate_field():
            self.field = None
        else:
            for ship in ships:
                current_ship = Ship(ship[0], ship[1])
                if ship[0][0] != ship[1][0]:
                    for row in range(ship[1][0] - ship[0][0] + 1):
                        self.field[(row + ship[0][0], ship[0][1])] \
                            = current_ship
                else:
                    for column in range(ship[1][1] - ship[0][1] + 1):
                        self.field[(ship[0][0], column + ship[0][1])] \
                            = current_ship

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                if (row, column) in self.field:
                    if (self.field[(row, column)]
                            .get_deck(row, column).is_alive):
                        print("□", end="\t")
                    elif (not self.field[(row, column)]
                            .get_deck(row, column).is_alive
                          and not self.field[(row, column)].is_drowned):
                        print("*", end="\t")
                    else:
                        print("X", end="\t")
                else:
                    print("~", end="\t")
            print()

    def _validate_field(self) -> bool:
        if len(self.ships) != 10:
            return False

        list_of_ships = [0, 0, 0, 0]
        for ship in self.ships:
            if ship[0][0] != ship[1][0]:
                list_of_ships[ship[1][0] - ship[0][0]] += 1
            elif ship[0][1] != ship[1][1]:
                list_of_ships[ship[1][1] - ship[0][1]] += 1
            else:
                list_of_ships[0] += 1

        return list_of_ships == [4, 3, 2, 1]

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"

        if self.field[location].is_last_deck():
            self.field[location].fire(location[0], location[1])
            return "Sunk!"

        self.field[location].fire(location[0], location[1])
        return "Hit!"
