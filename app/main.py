class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
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
        self.decks = self.create(start, end)
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> tuple:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        drowned = False
        deck = self.get_deck(row, column)
        if deck in self.decks:
            deck.is_alive = False
        for deck in self.decks:
            if deck.is_alive:
                drowned = True
        if not drowned:
            self.is_drowned = True

    @staticmethod
    def create(start: tuple, end: tuple) -> list:
        decks = []
        if start[0] == end[0]:
            for column in range(start[1], end[1] + 1):
                decks.append(Deck(start[0], column))
        elif start[1] == end[1]:
            for row in range(start[0], end[0] + 1):
                decks.append(Deck(row, end[1]))
        return decks


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = self.create_battle_field(ships)

    @staticmethod
    def create_battle_field(ships: list) -> dict:
        cell_dictionary = {}
        for ship in ships:
            new_ship = Ship(ship[0], ship[1])
            for deck in new_ship.decks:
                cell_dictionary[(deck.row, deck.column)] = new_ship
        return cell_dictionary

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            Ship.fire(ship, location[0], location[1])

            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def board_field(self, row: int, col: int) -> None:
        for i in range(row):
            for index in range(col):
                shipp = self.field.get((i, index))
                if ((i, index) in self.field
                        and shipp.get_deck(i, index).is_alive):
                    print(u"\u25A1", end=" ")
                    continue
                elif ((i, index) in self.field
                      and not shipp.get_deck(i, index).is_alive
                      and not shipp.is_drowned):
                    print("*", end=" ")
                    continue
                elif ((i, index) in self.field
                      and not shipp.get_deck(i, index).is_alive
                      and shipp.is_drowned):
                    print("x", end=" ")
                    continue
                print("~", end=" ")
            print()


if __name__ == "__main__":
    rows = 10
    cols = 10
    battle_ship = Battleship(
        ships=[
            ((0, 0), (0, 3)),
            ((0, 5), (0, 6)),
            ((0, 8), (0, 9)),
            ((2, 0), (4, 0)),
            ((2, 4), (2, 6)),
            ((2, 8), (2, 9)),
            ((9, 9), (9, 9)),
            ((7, 7), (7, 7)),
            ((7, 9), (7, 9)),
            ((9, 7), (9, 7)),
        ]
    )
    Battleship.board_field(battle_ship, rows, cols)
    battle = [(0, 4), (0, 3), (0, 2), (0, 1), (0, 0)]
    for hit in battle:
        print()
        print(battle_ship.fire(hit))
        Battleship.board_field(battle_ship, rows, cols)
