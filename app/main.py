class ValidationError(Exception):
    pass


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: list,
            end: list,
            is_drowned: bool = False
    ) -> None:
        if start[0] == end[0]:
            self.decks = [
                Deck(start[0], i)
                for i in range(start[1], end[1] + 1)
            ]
        if start[1] == end[1]:
            self.decks = [
                Deck(i, start[1])
                for i in range(start[0], end[0] + 1)
            ]
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        self.is_drowned = all([
            not deck.is_alive
            for deck in self.decks
        ])
        return "Sunk!" if self.is_drowned else "Hit!"


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {
            ship: Ship(*ship)
            for ship in ships
        }
        self._validate_field()

    def fire(self, loc: tuple) -> str:
        for coords, ship in self.field.items():
            ship_decks = ship.get_deck(*loc)
            if ship_decks is not None:
                return ship.fire(*loc)
        return "Miss!"

    def _validate_field(self) -> None:
        if len(self.field) != 10:
            raise ValidationError("Total amount of the ships should be 10")
        ships = [0] * 4
        for coords, ship in self.field.items():
            if coords[0] == coords[1]:
                ships[0] += 1
                continue
            diff = [coords[1][0] - coords[0][0], coords[1][1] - coords[0][1]]
            if diff[0] == 0:
                ships[diff[1]] += 1
            elif diff[1] == 0:
                ships[diff[0]] += 1

        if ships[0] != 4 or ships[1] != 3 or ships[2] != 2 or ships[3] != 1:
            raise ValidationError("there should be 4 single-deck ships\n"
                                  "there should be 3 double-deck ships\n"
                                  "there should be 2 three-deck ships\n"
                                  "there should be 1 four-deck ship"
                                  )

    def print_field(self) -> None:
        for _i in range(0, 10):
            for _k in range(0, 10):
                coord = (_i, _k)
                for coords, ship in self.field.items():
                    deck = ship.get_deck(*coord)
                    if deck is not None:
                        if ship.is_drowned:
                            print("x ", end="")
                            break
                        if not deck.is_alive:
                            print("* ", end="")
                            break
                        print(u"\u25A1 ", end="")
                        break
                else:
                    print("~ ", end="")
            print()
        print()
        return
