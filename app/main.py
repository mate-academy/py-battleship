from app.ship import Ship


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = ships
        self.field = {ship: Ship(*ship) for ship in self.ships}
        self.battle_field = self.create_field()

    def fire(self, location: tuple) -> str:
        for coordinates, ship in self.field.items():
            if location[0] in range(
                    coordinates[0][0], coordinates[1][0] + 1
            ) and location[1] in range(
                coordinates[0][1], coordinates[1][1] + 1
            ):
                ship.fire(*location)
                if ship.is_drowned:
                    for deck in ship.decks:
                        self.battle_field[deck.row][deck.column] = "x"
                    return "Sunk!"
                self.battle_field[location[0]][location[1]] = "*"
                return "Hit!"
        self.battle_field[location[0]][location[1]] = "o"
        return "Miss!"

    def create_field(self) -> list:
        battle_field = [["~" for _ in range(10)] for _ in range(10)]
        for ship in self.field.values():
            for deck in ship.decks:
                battle_field[deck.row][deck.column] = u"\u25A1"
        return battle_field

    def print_field(self) -> None:
        for row in self.battle_field:
            for column in row:
                print(column.rjust(2), end=" ")
            print()
