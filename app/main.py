class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        self.is_drowned = is_drowned
        self.decks = []

        if start[0] != end[0]:
            for row in range(start[0], end[0] + 1):
                self.decks.append(Deck(row, start[1]))

        elif start[1] != end[1]:
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], column))

        else:
            self.decks.append(Deck(start[0], start[1]))

    def get_deck(self, row: int, column: int) -> bool:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return True
        return False

    def fire(self, row: int, column: int) -> None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False
                if all([not deck.is_alive for deck in self.decks]):
                    self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}

        for ship in ships:
            ship_obj = Ship(*ship)
            self.field[
                tuple((deck.row, deck.column) for deck in ship_obj.decks)
            ] = ship_obj

    def fire(self, location: tuple) -> str:
        for value in self.field.values():
            if value.get_deck(*location):
                value.fire(*location)

                return "Sunk!" if value.is_drowned else "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        battle_field = [["~" for _ in range(10)] for _ in range(10)]

        for ship in self.field.values():
            if ship.is_drowned:
                for deck in ship.decks:
                    battle_field[deck.row][deck.column] = "X"

            elif not ship.is_drowned and all(
                    [deck.is_alive for deck in ship.decks]):
                for deck in ship.decks:
                    battle_field[deck.row][deck.column] = u"\u25A1"

            else:
                for deck in ship.decks:
                    battle_field[deck.row][
                        deck.column] = "*" if deck.is_alive else "X"

        for row in battle_field:
            print("     ".join(row))
